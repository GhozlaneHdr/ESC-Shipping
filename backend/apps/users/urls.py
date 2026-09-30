"""
URL configuration for user management.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomTokenObtainPairView,
    PublicUserView,
    UserProfileViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", UserProfileViewSet, basename="userprofile")

urlpatterns = [
    # User CRUD and profile endpoints
    path("", include(router.urls)),
    # Custom token endpoint with user data in response
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="custom_token_obtain_pair"),
    # Public registration endpoint
    path("auth/register/", PublicUserView.as_view(), name="public_register"),
]
