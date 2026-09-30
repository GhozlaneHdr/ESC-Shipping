from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MaritimeCampaignViewSet,
    AssociatedCampaignViewSet,
    ServiceViewSet,
    StatViewSet,
    TrustedPartnerViewSet,
)

app_name = "cms"

router = DefaultRouter()
router.register(r"maritime-campaigns", MaritimeCampaignViewSet, basename="maritime-campaign")
router.register(r"associated-campaigns", AssociatedCampaignViewSet, basename="associated-campaign")
router.register(r"services", ServiceViewSet, basename="service")
router.register(r"stats", StatViewSet, basename="stat")
router.register(r"partners", TrustedPartnerViewSet, basename="partner")

urlpatterns = [
    path("", include(router.urls)),
]
