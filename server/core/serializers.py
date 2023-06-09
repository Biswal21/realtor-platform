from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from .models import (
    ListingVideo,
    ListingImage,
    City,
    Region,
    CustomUser,
    Builder,
    Amenity,
    Listing,
    Coupon,
)
import re
import os
import random
import string
import datetime
import pytz

from drf_instamojo.models import Payment

from .utils import set_expiration_date


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(DynamicFieldsModelSerializer, self).get_field_names(
            declared_fields, info
        )

        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class CustomUserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "name",
            "alt_name",
            "email",
            "alt_email",
            "phone_number",
            "alt_phone_number",
            "modified_at",
            "created_at",
        ]

    def validate(self, data):
        print(data)
        if re.match(r"^[+]?[0-9]{9,15}$", data["phone_number"]) is None:
            print(data["phone_number"], type(data["phone_number"]))
            print("phone number validate")
            raise ValidationError({"Message": "phone number does not match the format"})
        if (
            data["alt_phone_number"] != ""
            and re.match(r"^[+]?[0-9]{9,15}$", data["phone_number"]) is None
        ):
            raise ValidationError(
                {"Message": "alternate phone number does not match the format"}
            )
        elif data["alt_phone_number"] == "":
            data["alt_phone_number"] = None

        # if CustomUser.objects.get(phone_number=data["phone_number"]):
        # This phone number is already registered

        return super().validate(data)


class CitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class RegionSerializer(DynamicFieldsModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = Region
        exclude = (
            "lft",
            "rght",
            "tree_id",
            "level",
        )
        write_only_fields = [
            "fk_city",
        ]

    def get_city(self, instance):
        return instance.fk_city.name


class BuilderSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Builder
        fields = "__all__"


class AmenitySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


# WHATS THIS?
class ListingSerializer(DynamicFieldsModelSerializer):
    property_usp = AmenitySerializer(many=True, read_only=True)
    fk_region = RegionSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "name",
            "dealer_approved",
            "property_usp",
            "premium_amount",
            "fk_builder",
            "fk_region",
            "modified_at",
            "created_at",
        ]
        depth = 1


class CouponSerializer(DynamicFieldsModelSerializer):
    is_expired = serializers.SerializerMethodField(method_name="get_expiration_date")
    listing_data = serializers.SerializerMethodField(method_name="get_listing_data")

    class Meta:
        model = Coupon
        fields = [
            "id",
            "name",
            "fk_user",
            "fk_listing",
            "listing_data",
            "fk_payment_request",
            "is_paid",
            "is_premium",
            "expiration_date",
            "is_expired",
            "modified_at",
            "created_at",
        ]
        read_only_fields = [
            "name",
            "is_premium",
            "listing_data",
            "fk_user",
            "is_paid",
            "fk_payment_request",
        ]

    def get_listing_data(self, instance):
        return {
            "id": instance.fk_listing.id,
            "name": instance.fk_listing.name,
            "region": instance.fk_listing.fk_region.name,
            "city": instance.fk_listing.fk_region.fk_city.name,
        }

    def get_expiration_date(self, instance):
        # print(
        #     instance.expiration_date, datetime.datetime.now().replace(tzinfo=pytz.UTC)
        # )
        # print(
        #     instance.expiration_date,
        #     "INSTANCE EXPIRATION DATE",
        #     instance.expiration_date.replace(tzinfo=pytz.UTC),
        # )
        if instance.expiration_date.replace(
            tzinfo=pytz.UTC
        ) >= datetime.datetime.now().replace(tzinfo=pytz.UTC):
            return False
        else:
            return True

    def create(self, validated_data):
        validated_data["name"] = (
            "Shelter"
            + "_"
            + "".join(random.choice(string.ascii_uppercase) for _ in range(6))
        )
        validated_data["is_premium"] = False
        validated_data["is_paid"] = False
        validated_data["expiration_date"] = set_expiration_date(
            int(os.getenv("COUPON_EXPIRATION_DAYS"))
        )
        request = self.context["request"]
        validated_data["fk_user"] = request.user
        return super().create(validated_data)


class DeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(source="customuser.phone_number")


class ResendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    is_signup = serializers.BooleanField()


class VerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()
    otp_size = serializers.IntegerField()

    def validate(self, attrs):
        if type(attrs["otp_size"]) is not int:
            raise ValidationError({"Message": "otp size invalid"})
        if not re.match(r"^\d{%d}$" % attrs["otp_size"], attrs["otp"]):
            raise ValidationError("otp invalid")
        return super().validate(attrs)


class CouponPaymentSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()

    def validate_listing_id(self, listing_id):
        try:
            listing = Listing.objects.get(id=listing_id)
            if listing.premium_amount is None:
                raise PermissionDenied("premium coupon does not exist for this listing")
        except Listing.DoesNotExist:
            raise NotFound("listing does not exist for given id")

        return listing_id


class UpdatedPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "payment_request"]


class ListingImageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ListingImage
        fields = [
            "id",
            "name",
            "fk_listing",
            "modified_at",
            "created_at",
        ]


class ListingVideoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ListingVideo
        fields = [
            "id",
            "name",
            "fk_listing",
            "modified_at",
            "created_at",
        ]


class ListingResponseSerializer(serializers.ModelSerializer):
    property_usp = AmenitySerializer(many=True, read_only=True)
    fk_region = RegionSerializer(read_only=True)
    listing_image = serializers.SerializerMethodField(method_name="get_listing_images")
    listing_video = serializers.SerializerMethodField(method_name="get_listing_videos")

    class Meta:
        model = Listing
        fields = [
            "id",
            "name",
            "dealer_approved",
            "property_usp",
            "listing_image",
            "listing_video",
            "premium_amount",
            "fk_builder",
            "fk_region",
            "premium_amount",
            "modified_at",
            "created_at",
            "display_image",
        ]
        depth = 1

    def get_listing_videos(self, instance):
        queryset = instance.listingvideo_set.all()
        return ListingVideoSerializer(queryset, many=True).data

    def get_listing_images(self, instance):
        queryset = instance.listingimage_set.all()
        return ListingImageSerializer(queryset, many=True).data
