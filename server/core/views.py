from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_spectacular.utils import extend_schema

from .serializers import (
    CustomUserSerializer,
    CitySerializer,
    RegionSerializer,
    BuilderSerializer,
    AmenitySerializer,
    ListingSerializer,
    ListingResponseSerializer,
    CouponSerializer,
    DeleteSerializer,
    LoginSerializer,
    ResendOtpSerializer,
    VerificationSerializer,
    UpdatedPaymentSerializer,
    CouponPaymentSerializer,
    # ListingImageSerializer,
    # ListingVideoSerializer,
)
from .models import (
    CustomUser,
    Coupon,
    City,
    # MessageTemplate,
    Region,
    Builder,
    Amenity,
    Listing,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_instamojo.serializers import (
    PaymentSerializer,
    PaymentRequestSerializer,
)
from drf_instamojo.models import PaymentRequest, Payment
from .utils import generate_otp_of_size, set_expiration_date, send_whatsapp_confirmation
from django.core.cache import cache

import datetime
import random
import string
import django_filters

# from django_filters import rest_framework as django_rest_filters
from .throttle import VerifyOTPThrottle, OTPGenerationThrottle
from django.core.mail import send_mail

import os

# Create your views here.

# [
#     Login,
#     Signup,
#     otp,
# ]

LOGIN_OTP_SIZE = int(os.getenv("LOGIN_OTP_SIZE"))
SIGNUP_OTP_SIZE = int(os.getenv("SIGNUP_OTP_SIZE"))


class UserViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="signup",
        permission_classes=[
            AllowAny,
        ],
    )
    def signup_verification(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "you are already logged in"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serialized = CustomUserSerializer(data=request.data)
        # print("HERE at 55")
        if serialized.is_valid():
            is_generated = generate_otp_of_size(SIGNUP_OTP_SIZE, serialized, None)

            if is_generated:
                ttl = cache.ttl(f'{serialized.validated_data["phone_number"]}')
                # otp = cache.get(f'{serialized.validated_data["phone_number"]}')["otp"]
                # subject = "welcome to ___ "
                # message = f'Hi {serialized.validated_data["name"]}, thank you for
                # registering in ___ . \n\nOTP: {otp}'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [
                #     serialized.validated_data["email"],
                #     serialized.validated_data["alt_email"],
                # ]
                # send_mail(subject, message, email_from, recipient_list)

                return Response(
                    {"ttl_otp": f"{ttl}", "otp_size": SIGNUP_OTP_SIZE},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "otp generation error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if serialized.errors["phone_number"][0].code == "unique":
            return Response(
                {"error": "This phone number is already registered"},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="login",
        permission_classes=[
            AllowAny,
        ],
        throttle_classes=[
            OTPGenerationThrottle,
        ],
    )
    def login_verification(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return Response(
                {"detail": "you are already logged in"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        serialized = LoginSerializer(data=request.data)

        if serialized.is_valid():
            try:
                print(type(serialized.validated_data["customuser"]["phone_number"]))
                CustomUser.objects.get(
                    phone_number=serialized.validated_data["customuser"]["phone_number"]
                )
            except CustomUser.DoesNotExist:
                return Response(
                    {"Error": "phone number not registered"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            phone_number = serialized.validated_data["customuser"]["phone_number"]
            is_generated = generate_otp_of_size(LOGIN_OTP_SIZE, None, phone_number)

            if is_generated:
                ttl = cache.ttl(
                    f'{serialized.validated_data["customuser"]["phone_number"]}'
                )

                # otp = cache.get(
                #     f'{serialized.validated_data["customuser"]["phone_number"]}'
                # )["otp"]
                # subject = "OTP verification"
                # message = f"Hi {user.name}, your otp is {otp}"
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [user.email, user.alt_email]
                # send_mail(subject, message, email_from, recipient_list)

                return Response(
                    {"ttl_otp": f"{ttl}", "otp_size": LOGIN_OTP_SIZE},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "otp generation error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(
        request=ResendOtpSerializer,
        responses={200: ResendOtpSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="resend_otp",
        permission_classes=[
            AllowAny,
        ],
    )
    def resend_otp(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "you are already logged in"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        serialized = ResendOtpSerializer(data=request.data)
        if serialized.is_valid():
            # print(serialized.validated_data)
            # print(serialized.validated_data["phone_number"])

            phone_number = serialized.validated_data["phone_number"]
            user = cache.get(f"{phone_number}")

            if user is None:
                if serialized.validated_data["is_signup"]:
                    return Response(
                        {"error": "Bad signup request"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    {"error": "Bad login request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            else:
                if serialized.validated_data["is_signup"]:
                    is_generated = generate_otp_of_size(
                        SIGNUP_OTP_SIZE, user["serialized"], None
                    )
                else:
                    is_generated = generate_otp_of_size(
                        LOGIN_OTP_SIZE, None, phone_number
                    )

            if is_generated:
                ttl = cache.ttl(f"{phone_number}")
                otp = cache.get(f"{phone_number}")["otp"]
                subject = "OTP verification"
                message = f"Hi, your otp is {otp}"
                email_from = settings.EMAIL_HOST_USER

                if serialized.validated_data["is_signup"]:
                    recipient_list = [
                        user["serialized"].data["email"],
                        user["serialized"].data["email"],
                    ]
                    send_mail(subject, message, email_from, recipient_list)
                    return Response(
                        {"ttl_otp": f"{ttl}", "otp_size": SIGNUP_OTP_SIZE},
                        status=status.HTTP_200_OK,
                    )
                else:
                    try:
                        user = CustomUser.objects.get(phone_number=phone_number)
                    except CustomUser.DoesNotExist:
                        return Response(
                            {"Error": "phone number not registered"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    recipient_list = [user.email, user.alt_email]
                    send_mail(subject, message, email_from, recipient_list)
                    return Response(
                        {"ttl_otp": f"{ttl}", "otp_size": LOGIN_OTP_SIZE},
                        status=status.HTTP_200_OK,
                    )

                ttl = cache.ttl(f"{phone_number}")
                return Response({"ttl_otp": f"{ttl}"})
            return Response(
                {"error": "otp generation error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(
        request=VerificationSerializer,
        responses={200: CustomUserSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="verify_otp",
        permission_classes=[
            AllowAny,
        ],
        throttle_classes=[
            VerifyOTPThrottle,
        ],
    )
    def otp_verification(self, request):
        if request.user.is_authenticated:
            return Response(
                {"detail": "you are already verified"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        serialized = VerificationSerializer(data=request.data)

        if serialized.is_valid():
            # if cache.get(f'{serialized.validated_data["phone_number"]}'):
            if serialized.validated_data["phone_number"] in cache:
                user_data = cache.get(f'{serialized.validated_data["phone_number"]}')

                print(user_data["otp"])
                print(serialized.validated_data["otp"])

                if user_data["otp"] == serialized.validated_data["otp"]:
                    if "serialized" in user_data:
                        user_data["serialized"].save()

                    user = CustomUser.objects.get(
                        phone_number=serialized.validated_data["phone_number"]
                    )
                    token = RefreshToken.for_user(user)
                    data = {"refresh": str(token), "access": str(token.access_token)}
                    # erase cache for this phone number
                    return Response(data=data, status=status.HTTP_200_OK)

                elif user_data["otp"] != serialized.validated_data["otp"]:
                    ttl = cache.ttl(f'{serialized.validated_data["phone_number"]}')
                    return Response(
                        {"otp_mismatch": f"{ttl}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "otp expired, resend otp"}, status=status.HTTP_410_GONE
                )

        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # logout def
    @extend_schema(
        request=TokenRefreshSerializer, responses={200: TokenRefreshSerializer}
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="refresh",
        permission_classes=[
            AllowAny,
        ],
    )
    def token_refresh(self, request):
        serialized = TokenRefreshSerializer(data=request.data)

        try:
            if serialized.is_valid():
                # print(serialized.validated_data)
                # token = RefreshToken(serialized.validated_data['refresh'])
                # data = {"access": str(token.access_token)}

                return Response(
                    data=serialized.validated_data, status=status.HTTP_200_OK
                )
        except Exception:
            return Response(
                {"token_error": "Token is blacklisted"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        print(serialized.errors)
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @extend_schema(request=TokenRefreshSerializer, responses={200})
    @action(
        detail=False,
        methods=["post"],
        url_path="logout",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    # add later isAuthenticated
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            try:
                token = RefreshToken(refresh_token)
            except Exception:
                return Response(
                    {"token_error": "Token is blacklisted"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            token.blacklist()

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e, type(e))

            return Response(status=status.HTTP_400_BAD_REQUEST)


class CouponUtilityViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: CouponSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def read_coupons(self, request):
        if request.user.is_authenticated:
            try:
                coupon_list = Coupon.objects.filter(fk_user=request.user).order_by(
                    "-created_at"
                )
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = CouponSerializer(instance=coupon_list, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CustomUserViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_user(self, request):
        serialized = CustomUserSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CustomUserSerializer},
    )
    @action(detail=True, methods=["get"], url_path="read")
    def read_user(self, request, pk):
        try:
            query = CustomUser.objects.get(id=pk)

        except CustomUser.DoesNotExist:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CustomUserSerializer(instance=query)
            else:
                serialized = CustomUserSerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: CustomUserSerializer},
    )
    @action(detail=False, methods=["get"], url_path="read")
    def read_users(self, request):
        queryset = CustomUser.objects.all()
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CustomUserSerializer(instance=queryset, many=True)
            else:
                serialized = CustomUserSerializer(
                    instance=queryset, fields=fields, many=True
                )

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CustomUserSerializer,
        responses={200: CustomUserSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_user(self, request):
        try:
            user_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = CustomUser.objects.get(id=user_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = CustomUserSerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_users(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            users = CustomUser.objects.filter(id__in=request.data["ids"])

            try:
                users.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CityViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CitySerializer,
        responses={201: CitySerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_cities(self, request):
        serialized = CitySerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CitySerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_city(self, request, pk):
        try:
            query = City.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CitySerializer(instance=query)
            else:
                serialized = CitySerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: CitySerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_cities(self, request):
        queryset = City.objects.all().order_by("name")
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CitySerializer(instance=queryset, many=True)
            else:
                serialized = CitySerializer(instance=queryset, fields=fields, many=True)

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CitySerializer,
        responses={200: CitySerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_city(self, request):
        try:
            listing_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = City.objects.get(id=listing_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = CitySerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_cities(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            listings = City.objects.filter(id__in=request.data["ids"])

            try:
                listings.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionFilter(django_filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            "id": ["exact"],
            "name": ["exact"],
            "fk_city": ["exact"],
        }


class RegionViewSet(viewsets.ViewSet):
    @extend_schema(
        request=RegionSerializer,
        responses={201: RegionSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_regions(self, request):
        serialized = RegionSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: RegionSerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_region(self, request, pk):
        try:
            query = Region.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = RegionSerializer(instance=query)
            else:
                serialized = RegionSerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: RegionSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_regions(self, request):
        queryset = RegionFilter(
            request.GET, queryset=Region.objects.all().order_by("name")
        ).qs
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = RegionSerializer(instance=queryset, many=True)
            else:
                serialized = RegionSerializer(
                    instance=queryset, fields=fields, many=True
                )

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=RegionSerializer,
        responses={200: RegionSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_region(self, request):
        try:
            listing_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = Region.objects.get(id=listing_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = CitySerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_regions(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            listings = Region.objects.filter(id__in=request.data["ids"])

            try:
                listings.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class BuilderViewSet(viewsets.ViewSet):
    @extend_schema(
        request=BuilderSerializer,
        responses={201: BuilderSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_builders(self, request):
        serialized = BuilderSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: BuilderSerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_builder(self, request, pk):
        try:
            query = Builder.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = BuilderSerializer(instance=query)
            else:
                serialized = BuilderSerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: BuilderSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_builders(self, request):
        queryset = Builder.objects.all()
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = BuilderSerializer(instance=queryset, many=True)
            else:
                serialized = BuilderSerializer(
                    instance=queryset, fields=fields, many=True
                )

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=BuilderSerializer,
        responses={200: BuilderSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_builder(self, request):
        try:
            builder_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = Builder.objects.get(id=builder_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = BuilderSerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_builders(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            builders = Builder.objects.filter(id__in=request.data["ids"])

            try:
                builders.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(
        field_name="author__last_name", lookup_expr="iexact"
    )
    id = django_filters.NumberFilter(field_name="id", lookup_expr="iexact")

    class Meta:
        model = Listing

        fields = {"id": ["exact"], "name": ["exact"], "fk_region_id": ["exact"]}
        strict = True


class ListingViewSet(viewsets.ViewSet):
    @extend_schema(
        request=ListingSerializer,
        responses={201: ListingSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_listings(self, request):
        serialized = ListingSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: ListingSerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_listing(self, request, pk):
        try:
            query = Listing.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = ListingResponseSerializer(instance=query)
            else:
                serialized = ListingResponseSerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: ListingSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            AllowAny,
        ],
    )
    def read_listings(self, request):
        queryset = ListingFilter(request.GET, queryset=Listing.objects.all()).qs
        print(queryset)

        serialized = ListingResponseSerializer(instance=queryset, many=True)

        # if serialized.is_valid():

        #     return Response(
        #         {"detail": "Serializer Error"},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ListingSerializer,
        responses={200: ListingSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_listing(self, request):
        try:
            listing_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = Listing.objects.get(id=listing_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = ListingSerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_listings(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            listings = Listing.objects.filter(id__in=request.data["ids"])

            try:
                listings.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class AmenityViewSet(viewsets.ViewSet):
    @extend_schema(
        request=AmenitySerializer,
        responses={201: AmenitySerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_amenities(self, request):
        serialized = AmenitySerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: AmenitySerializer},
    )
    @action(detail=True, methods=["get"], url_path="read")
    def read_amenity(self, request, pk):
        try:
            query = Amenity.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = AmenitySerializer(instance=query)
            else:
                serialized = AmenitySerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: AmenitySerializer},
    )
    @action(detail=False, methods=["get"], url_path="read")
    def read_amenities(self, request):
        queryset = Amenity.objects.all()
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = AmenitySerializer(instance=queryset, many=True)
            else:
                serialized = AmenitySerializer(
                    instance=queryset, fields=fields, many=True
                )

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=AmenitySerializer,
        responses={200: AmenitySerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_amenity(self, request):
        try:
            amenity_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = Listing.objects.get(id=amenity_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = AmenitySerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_amenities(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            amenities = Amenity.objects.filter(id__in=request.data["ids"])

            try:
                amenities.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CouponViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CouponSerializer,
        responses={201: CouponSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="create",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def create_coupon(self, request):
        try:
            free_coupons = Coupon.objects.filter(
                fk_user__exact=request.user.id, is_premium=False
            ).filter(expiration_date__gte=datetime.datetime.now())
        except Exception:
            pass

        if len(free_coupons) >= int(os.getenv("FREE_COUPON_LIMIT")):
            print("free coupon limit reached")
            return Response(
                {"message": "You have reached the maximum number of free coupons"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serialized = CouponSerializer(data=request.data, context={"request": request})

        if serialized.is_valid():
            try:
                try:
                    coupon = Coupon.objects.get(
                        fk_user__exact=request.user.id,
                        fk_listing__exact=serialized.validated_data["fk_listing"],
                    )

                    if coupon.name == "":
                        coupon.name = (
                            "Shelter"
                            + "_"
                            + "".join(
                                random.choice(string.ascii_uppercase) for _ in range(6)
                            )
                        )

                        coupon.is_premium = False
                        coupon.is_paid = False
                        coupon.expiration_date = set_expiration_date(
                            int(os.getenv("COUPON_EXPIRATION_DAYS"))
                        )
                        coupon.save()
                        serialized_update = CouponSerializer(instance=coupon)
                        confirmation_template = os.environ.get(
                            "WHATSAPP_DEFAULT_MESSAGE_TEMPLATE"
                        )
                        status_code, response = send_whatsapp_confirmation(
                            coupon.fk_user.phone_number, confirmation_template, coupon
                        )
                        return Response(
                            data=serialized_update.data, status=status.HTTP_200_OK
                        )
                except Coupon.DoesNotExist:
                    pass

                coupon = serialized.save()
                # try:
                #     confirmation_template = MessageTemplate.objects.get(is_active=True) # noqa
                # except MessageTemplate.DoesNotExist:
                #     confirmation_template = os.environ.get(
                #         "WHATSAPP_DEFAULT_MESSAGE_TEMPLATE"
                #     )
                confirmation_template = os.environ.get(
                    "WHATSAPP_DEFAULT_MESSAGE_TEMPLATE"
                )
                status_code, response = send_whatsapp_confirmation(
                    coupon.fk_user.phone_number, confirmation_template, coupon
                )
                print("Print Whatsapp Status Code: ", status_code, response)

            except IntegrityError:
                return Response(
                    {"message": "You have already generated coupon for this listing"},
                    status=status.HTTP_409_CONFLICT,
                )

            return Response(data=serialized.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: CouponSerializer},
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="read",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def read_coupon(self, request, pk):
        try:
            query = Coupon.objects.get(id=pk)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user.id != query.fk_user.id:
            return Response(
                {"message": "You are not authorized to view this coupon"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CouponSerializer(instance=query)
            else:
                serialized = CouponSerializer(instance=query, fields=fields)
        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: CouponSerializer},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="read",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def read_coupons(self, request):
        queryset = Coupon.objects.filter(fk_user=request.user.id).order_by(
            "-created_at"
        )
        fields = self.request.query_params.getlist("fields", "")

        try:
            if fields == "":
                serialized = CouponSerializer(instance=queryset, many=True)
            else:
                serialized = CouponSerializer(
                    instance=queryset, fields=fields, many=True
                )

        except Exception:
            return Response(
                {"detail": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CouponSerializer,
        responses={200: CouponSerializer},
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path="update",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def update_coupon(self, request):
        try:
            listing_id = request.data["id"]

        except Exception:
            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            query = Coupon.objects.get(id=listing_id)

        except Exception:
            return Response(
                {"message": "id does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized = CouponSerializer(query, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=DeleteSerializer,
        responses={204: DeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_coupons(self, request):
        serialized = DeleteSerializer(data=request.data)

        if serialized.is_valid():
            listings = Coupon.objects.filter(id__in=request.data["ids"])

            try:
                listings.delete()
            except Exception:
                return Response(
                    {"message": "Internal Server Error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ViewSet):
    @extend_schema(
        request=CouponPaymentSerializer,
        responses={200: CouponPaymentSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="payment",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def coupon_payment(self, request):
        user = CustomUser.objects.get(
            phone_number__exact=self.request.user.phone_number
        )
        serialized = CouponPaymentSerializer(data=request.data)
        if serialized.is_valid():
            listing = Listing.objects.get(
                id__exact=serialized.validated_data["listing_id"]
            )

            try:
                coupon = Coupon.objects.get(
                    fk_user__exact=user, fk_listing__exact=listing
                )
                if coupon.is_premium is not False and coupon.name != "":
                    return Response(
                        {"detail": "coupon already generated"},
                        status=status.HTTP_409_CONFLICT,
                    )
                if coupon.name == "":
                    coupon.delete()
                    coupon = False

            except Coupon.DoesNotExist:
                coupon = False
                pass

            amount = listing.premium_amount
            if amount is None:
                return Response(
                    {"detail": "premium not available for current listing"},
                    status=status.HTTP_200_OK,
                )
            prs = PaymentRequestSerializer(
                data={
                    "amount": round(amount, 2),
                    "purpose": "Coupon for - " + listing.name,
                    "send_sms": False,
                    "redirect_url": "http://139.59.23.157:8000/core/payment/payment",
                    "allow_repeated_payments": False,
                    "email": user.email,
                    "buyer_name": user.name,
                }
            )
            if prs.is_valid(raise_exception=True):
                prs.save(created_by_id=user.id)
            print(prs.data)
            payment_request = PaymentRequest.objects.get(id__exact=prs.data["id"])

            if coupon:
                coupon.fk_payment_request = payment_request.id
            else:
                coupon = Coupon(
                    name="",
                    fk_user=user,
                    fk_listing=listing,
                    fk_payment_request=payment_request.id,
                    is_premium=True,
                )
            coupon.save()

            print(prs.data)
            return Response(
                {
                    "listing_id": listing.id,
                    "name": listing.name,
                    "cost": amount,
                    "payable_amount": round(amount, 2),
                    "payment_url": prs.data.get("longurl"),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class UpdatedPaymentViewSet(viewsets.ViewSet):
    @extend_schema(
        responses={200: UpdatedPaymentSerializer},
    )
    @action(detail=False, methods=["get"], url_path="payment")
    def update_payment(self, request):
        ps = PaymentSerializer(
            data={
                "id": request.query_params["payment_id"],
                "payment_request": request.query_params["payment_request_id"],
            }
        )
        ps.is_valid(raise_exception=True)
        print(ps.validated_data)
        ps.save()
        payment = Payment.objects.get(id=ps.data["id"])

        if payment.status == "Credit":
            coupon = Coupon.objects.get(
                fk_payment_request__exact=payment.payment_request.id
            )
            coupon.is_premium = True
            coupon.is_paid = True
            coupon.name = (
                "Shelter"
                + "_PREMIUM_"
                + "".join(random.choice(string.ascii_uppercase) for _ in range(6))
            )
            coupon.expiration_date = set_expiration_date(
                int(os.getenv("COUPON_EXPIRATION_DAYS"))
            )

            coupon.save()
            # try:
            #     confirmation_template = MessageTemplate.objects.get(is_active=True) # noqa
            # except MessageTemplate.DoesNotExist:
            #     confirmation_template = os.environ.get(
            #         "WHATSAPP_DEFAULT_MESSAGE_TEMPLATE"
            #     )
            confirmation_template = os.environ.get("WHATSAPP_DEFAULT_MESSAGE_TEMPLATE")
            status_code, response_message = send_whatsapp_confirmation(
                coupon.fk_user.phone_number, confirmation_template, coupon
            )
            print("Print Whatsapp Status Code: ", status_code, response_message)
            # if status_code == 404:
            #     return Response(
            #         {"message":
            # f"{response_message['error']['error_data']['details']}"}, #noqa
            #         status=status.HTTP_404_NOT_FOUND,
            #     )
            return redirect("http://139.59.23.157:3000/coupon/")

        else:
            coupon = Coupon.objects.get(
                fk_payment_request__exact=payment.payment_request.id
            )
            if coupon.name == "":
                coupon.delete()
            else:
                coupon.is_premium = False
                coupon.fk_payment_request = None
                coupon.is_paid = False
                coupon.save()
            return Response(
                {"message": "Payment failed, retry payment request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # return Response(
        #     data=serialized.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        # )
