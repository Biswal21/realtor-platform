from rest_framework import routers

from .views import (
    UserViewSet,
    CustomUserViewSet,
    CityViewSet,
    RegionViewSet,
    BuilderViewSet,
    ListingViewSet,
    AmenityViewSet,
    CouponViewSet,
    PaymentViewSet,
    UpdatedPaymentViewSet,
    CouponUtilityViewSet,
)

router = routers.DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
router.register(r"custom_user", CustomUserViewSet, basename="custom_user")
router.register(r"city", CityViewSet, basename="city")
router.register(r"region", RegionViewSet, basename="region")
router.register(r"builder", BuilderViewSet, basename="builder")
router.register(r"listing", ListingViewSet, basename="listing")
router.register(r"amenity", AmenityViewSet, basename="amenity")
router.register(r"coupon", CouponViewSet, basename="coupon")
router.register(r"payment_request", PaymentViewSet, basename="payment_request")
router.register(r"payment", UpdatedPaymentViewSet, basename="payment")
router.register(r"user_coupons", CouponUtilityViewSet, basename="user_coupons")

urlpatterns = router.urls
