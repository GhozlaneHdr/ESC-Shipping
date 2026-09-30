from rest_framework import viewsets, permissions
from .models import MaritimeCampaign, AssociatedCampaign, Service, Stat, TrustedPartner
from .serializers import (
    MaritimeCampaignSerializer,
    AssociatedCampaignSerializer,
    ServiceSerializer,
    StatSerializer,
    TrustedPartnerSerializer,
)

# Using ReadOnlyModelViewSet because content is managed via Django Admin
# and the frontend only needs GET access to display it.

class MaritimeCampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for fetching published maritime campaigns."""
    queryset = MaritimeCampaign.objects.filter(is_published=True)
    serializer_class = MaritimeCampaignSerializer
    permission_classes = [permissions.AllowAny]


class AssociatedCampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for fetching published associated campaigns."""
    queryset = AssociatedCampaign.objects.filter(is_published=True)
    serializer_class = AssociatedCampaignSerializer
    permission_classes = [permissions.AllowAny]


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for fetching active services."""
    queryset = Service.objects.filter(is_active=True).prefetch_related("steps")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"  # Allow looking up services by /api/cms/services/slug-name/


class StatViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for company physical stats."""
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # Return all stats at once without pagination


class TrustedPartnerViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for active trusted partners/logos."""
    queryset = TrustedPartner.objects.filter(is_active=True)
    serializer_class = TrustedPartnerSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # No pagination required for marquee logos
