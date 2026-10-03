"""
Views for CMS models (Services, Campaigns, Stats, Partners).
"""

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import (
    AssociatedCampaign,
    MaritimeCampaign,
    Service,
    SiteBranding,
    Stat,
    TrustedPartner,
)
from .serializers import (
    AssociatedCampaignSerializer,
    MaritimeCampaignSerializer,
    ServiceSerializer,
    SiteBrandingSerializer,
    StatSerializer,
    TrustedPartnerSerializer,
)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for services."""

    queryset = Service.objects.filter(is_active=True).prefetch_related("steps")
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class SiteBrandingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteBranding.objects.all()
    serializer_class = SiteBrandingSerializer
    permission_classes = [AllowAny]


class MaritimeCampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for maritime campaigns."""

    queryset = MaritimeCampaign.objects.filter(is_published=True)
    serializer_class = MaritimeCampaignSerializer
    permission_classes = [AllowAny]


class AssociatedCampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for associated campaigns."""

    queryset = AssociatedCampaign.objects.filter(is_published=True)
    serializer_class = AssociatedCampaignSerializer
    permission_classes = [AllowAny]


class StatViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for company statistics."""

    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = [AllowAny]


class TrustedPartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for trusted partners."""

    queryset = TrustedPartner.objects.filter(is_active=True)
    serializer_class = TrustedPartnerSerializer
    permission_classes = [AllowAny]
