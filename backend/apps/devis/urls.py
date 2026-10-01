"""
URL configuration for Devis management.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DevisViewSet

router = DefaultRouter()
router.register(r"devis", DevisViewSet, basename="devis")

urlpatterns = [
    path("", include(router.urls)),
]
