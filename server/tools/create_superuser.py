import os
from django.contrib.auth import get_user_model

User = get_user_model()

DJANGO_SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME")
DJANGO_SUPERUSER_ALT_NAME = os.environ.get("DJANGO_SUPERUSER_ALT_NAME")
DJANGO_SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL")
DJANGO_SUPERUSER_ALT_EMAIL = os.environ.get("DJANGO_SUPERUSER_ALT_EMAIL")
DJANGO_SUPERUSER_PHONE_NUMBER = os.environ.get("DJANGO_SUPERUSER_PHONE_NUMBER")
DJANGO_SUPERUSER_ALT_PHONE_NUMBER = os.environ.get("DJANGO_SUPERUSER_ALT_PHONE_NUMBER")
DJANGO_SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD")


if User.objects.filter(phone_number=DJANGO_SUPERUSER_USERNAME).exists():
    print("Superuser is already initialized!")
else:
    print("Initializing superuser...")
    try:
        superuser = User.objects.create_superuser(
            name=DJANGO_SUPERUSER_USERNAME,
            alt_name=DJANGO_SUPERUSER_ALT_NAME,
            phone_number=DJANGO_SUPERUSER_PHONE_NUMBER,
            alt_phone_number=DJANGO_SUPERUSER_ALT_PHONE_NUMBER,
            email=DJANGO_SUPERUSER_EMAIL,
            alt_email=DJANGO_SUPERUSER_ALT_EMAIL,
            password=DJANGO_SUPERUSER_PASSWORD,
        )
        superuser.save()
        print("Superuser initialized!")
    except Exception as e:
        print(e)
