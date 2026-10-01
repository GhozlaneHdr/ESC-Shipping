"""
URL configuration for Shipping management.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PackageViewSet, ShipmentViewSet, TrackingEventViewSet

router = DefaultRouter()
router.register(r"shipments", ShipmentViewSet, basename="shipment")
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"tracking-events", TrackingEventViewSet, basename="tracking-event")

urlpatterns = [
    path("", include(router.urls)),
]
