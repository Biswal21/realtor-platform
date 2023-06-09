# from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from .storage_backends import PublicMediaStorage


# Create your models here.
phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="""Phone number must be entered in the format: '+999999999'.
    Up to 15 digits allowed.""",
)


class ListingVideo(models.Model):
    name = models.URLField()
    fk_listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ListingImage(models.Model):
    name = models.FileField(storage=PublicMediaStorage())
    fk_listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.fk_listing.name}"


class City(models.Model):
    name = models.CharField(max_length=254)
    city_image = models.FileField(storage=PublicMediaStorage())
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"


class Region(MPTTModel):
    name = models.CharField(max_length=254)
    fk_city = models.ForeignKey("City", on_delete=models.CASCADE)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        name,
        alt_name,
        email,
        alt_email,
        phone_number,
        alt_phone_number,
        **other_fields,
    ):
        values = [name, alt_name, email, alt_email, phone_number, alt_phone_number]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f"The {field_name} value must be set")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            alt_name=alt_name,
            alt_email=self.normalize_email(alt_email),
            phone_number=phone_number,
            alt_phone_number=alt_phone_number,
            **other_fields,
        )
        if other_fields.get("is_superuser"):
            if "password" not in other_fields or other_fields.get("password") == "":
                raise ValueError("Superuser must have a password")
            user.set_password(other_fields.get("password"))

        user.save(using=self._db)
        return user

    def create_user(
        self,
        name,
        alt_name,
        email,
        alt_email,
        phone_number,
        alt_phone_number,
        **other_fields,
    ):
        other_fields.setdefault("is_superuser", False)
        return self._create_user(
            name,
            alt_name,
            email,
            alt_email,
            phone_number,
            alt_phone_number,
            **other_fields,
        )

    def create_superuser(
        self,
        name,
        alt_name,
        email,
        alt_email,
        phone_number,
        alt_phone_number,
        **other_fields,
    ):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        other_fields.setdefault("is_staff", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if "password" not in other_fields or other_fields.get("password") == "":
            raise ValueError("Superuser must have a password")

        return self._create_user(
            name,
            alt_name,
            email,
            alt_email,
            phone_number,
            alt_phone_number,
            **other_fields,
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    alt_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    alt_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True
    )
    alt_phone_number = models.CharField(
        validators=[phone_regex], max_length=17, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    REQUIRED_FIELDS = ["name", "alt_name", "email", "alt_email"]

    USERNAME_FIELD = "phone_number"

    def get_phone(self):
        return self.phone_number

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Builder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Property USP"

    def __str__(self):
        return self.name


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    dealer_approved = models.BooleanField(default=False)
    property_usp = models.ManyToManyField("Amenity", blank=True)
    fk_builder = models.ForeignKey("Builder", on_delete=models.SET_NULL, null=True)
    fk_region = models.ForeignKey("Region", on_delete=models.SET_NULL, null=True)
    premium_amount = models.FloatField(null=True, default=9999.99)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    display_image = models.FileField(
        storage=PublicMediaStorage(), null=True, blank=True
    )

    def __str__(self):
        return self.name


class Coupon(models.Model):
    name = models.CharField(max_length=254, unique=True)
    fk_user = models.ForeignKey("CustomUser", on_delete=models.DO_NOTHING)
    fk_listing = models.ForeignKey(
        "Listing", on_delete=models.SET_NULL, null=True, blank=True
    )
    fk_payment_request = models.CharField(
        max_length=254, null=True, verbose_name=("Payment Request ID")
    )
    is_premium = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(null=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("fk_listing", "fk_user")


class MessageTemplate(models.Model):
    template_name = models.CharField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.is_active:
            active_count = (
                MessageTemplate.objects.filter(is_active=True)
                .exclude(pk=self.pk)
                .count()
            )
            if active_count > 0:
                raise ValidationError("Only one row can be active at a time.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.template_name
