# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenViewBase
# from django.contrib.auth.backends import BaseBackend, ModelBackend
# from core.models import CustomUser
# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

# class TokenObtainPairOtpSerializer(TokenObtainPairSerializer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         print(self.fields)
#         self.fields["otp"] = serializers.CharField()
#         # self.fields[self.otp] = serializers.CharField()
#         self.fields["password"].required = False

#     def validate(self, attrs):
#         attrs.update({"password": ""})
#         return super(TokenObtainPairOtpSerializer, self).validate(attrs)


# class TokenObtainPairOtpView(TokenViewBase):
#     serializer_class = TokenObtainPairOtpSerializer


# class AuthenticationOtp(BaseBackend):
#     def authenticate(self, request=None, otp=None, **other_fields):

#         if 'username' in other_fields:
#             username = other_fields['username']
#             if 'password' in other_fields:
#                 password = other_fields['password']
#             else:
#                 password = None
#             if username is None:
#                 username = other_fields.get(UserModel.USERNAME_FIELD)

#             if username is None or password is None:
#                 return
#             user = None
#             try:
#                 user = UserModel.objects.get(phone_number=username)

#             except UserModel.DoesNotExist:
#                 # Run the default password hasher once to reduce the timing
#                 # difference between an existing and a nonexistent user (#20760).
#                 UserModel().set_password(password)

#             if user and user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#             else:
#                 return

#         if 'phone_number' in other_fields:
#             phone_number = request.data.get("phone_number", "")
#         try:
#             user = CustomUser.objects.get(phone_number=phone_number)
#             if otp is None:
#                 otp = request.data["otp"]

#             if otp != "69420":
#                 return None

#             return user

#         except CustomUser.DoesNotExist:
#             return None

#     def get_user(self, id):
#         try:
#             return CustomUser.objects.get(pk=id)
#         except CustomUser.DoesNotExist:
#             return None
