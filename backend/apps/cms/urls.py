"""
URL configuration for CMS API endpoints.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AssociatedCampaignViewSet,
    MaritimeCampaignViewSet,
    ServiceViewSet,
    SiteBrandingViewSet,
    StatViewSet,
    TrustedPartnerViewSet,
    ResourceItemViewSet,
)

router = DefaultRouter()
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"branding", SiteBrandingViewSet, basename="branding")
router.register(r"maritime-campaigns", MaritimeCampaignViewSet, basename="maritime-campaign")
router.register(r"associated-campaigns", AssociatedCampaignViewSet, basename="associated-campaign")
router.register(r"stats", StatViewSet, basename="stat")
router.register(r"partners", TrustedPartnerViewSet, basename="partner")
router.register(r"resources", ResourceItemViewSet, basename="resource")

urlpatterns = [
    path("", include(router.urls)),
]
