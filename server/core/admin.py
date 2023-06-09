from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser,
    Amenity,
    Builder,
    City,
    Coupon,
    Listing,
    ListingImage,
    ListingVideo,
    MessageTemplate,
    Region,
)
from .forms import UserCreationForm, UserChangeForm


class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "name",
        "alt_name",
        "email",
        "alt_email",
        "phone_number",
        "alt_phone_number",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_superuser",)

    fieldsets = (
        (None, {"fields": ("phone_number", "is_superuser")}),
        (
            "Personal info",
            {"fields": ("name", "alt_name", "email", "alt_email", "alt_phone_number")},
        ),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )
    add_fieldsets = (
        (None, {"fields": ("phone_number", "is_superuser")}),
        (
            "Personal info",
            {"fields": ("name", "alt_name", "email", "alt_email", "alt_phone_number")},
        ),
        ("Groups", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("user_permissions",)}),
    )

    search_fields = ("email", "name", "phone")
    ordering = ("email",)
    filter_horizontal = ()


class AmenityAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_per_page = 50


class ListingImageInline(admin.TabularInline):
    model = ListingImage


class ListingVideoInline(admin.StackedInline):
    model = ListingVideo


class ListingAdmin(admin.ModelAdmin):
    inlines = [
        ListingImageInline,
        ListingVideoInline,
    ]


admin.site.register(CustomUser, AccountAdmin)


admin.site.register(Builder)
admin.site.register(Amenity, AmenityAdmin)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Coupon)
admin.site.register(ListingImage)
admin.site.register(ListingVideo)
admin.site.register(MessageTemplate)
