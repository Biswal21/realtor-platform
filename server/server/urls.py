"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# from drf_instamojo.views import ListAddPaymentRequestView, ListAddPaymentView
from drf_spectacular import openapi

# from .jwt_config import TokenObtainPairOtpView
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Server API",
#       default_version='v1',
#       description="API Explorer for Server",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="google@google.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path(r"schema/", SpectacularAPIView.as_view(), name="schema"),
    # path('api/token/', TokenObtainPairOtpView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # path('api/instamojo/', include('drf_instamojo.urls')),
]

urlpatterns += [
    # Admin endpoint
    path("admin/", admin.site.urls),
    # Auth endpoints
    # url(r'^auth/', include('djoser.urls')),
    url(r"^auth/", include("djoser.urls.jwt")),
    path("core/", include("core.urls")),
]
