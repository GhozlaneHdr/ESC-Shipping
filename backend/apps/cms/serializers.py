"""
Serializers for CMS models (Services, Campaigns, Stats, Partners).
"""

from rest_framework import serializers

from .models import (
    AssociatedCampaign,
    MaritimeCampaign,
    Service,
    ServiceStep,
    SiteBranding,
    Stat,
    TrustedPartner,
    ResourceItem,
)


class ServiceStepSerializer(serializers.ModelSerializer):
    """Serializer for service steps."""

    class Meta:
        model = ServiceStep
        fields = ["id", "title", "text", "order"]


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for services with nested steps."""

    steps = ServiceStepSerializer(many=True, read_only=True)
    benefits_list = serializers.SerializerMethodField()
    why_us_list = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "slug",
            "name",
            "short_description",
            "long_intro",
            "image",
            "benefits",
            "benefits_list",
            "why_us",
            "why_us_list",
            "steps",
            "is_active",
            "order",
        ]

    def get_benefits_list(self, obj):
        return [line.strip() for line in obj.benefits.split("\n") if line.strip()]

    def get_why_us_list(self, obj):
        return [line.strip() for line in obj.why_us.split("\n") if line.strip()]


class SiteBrandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteBranding
        fields = ["id", "logo", "hero_video"]


class MaritimeCampaignSerializer(serializers.ModelSerializer):
    """Serializer for maritime campaigns."""

    highlights_list = serializers.SerializerMethodField()

    class Meta:
        model = MaritimeCampaign
        fields = [
            "id",
            "title",
            "subtitle",
            "route_from",
            "route_to",
            "discount",
            "description",
            "highlights",
            "highlights_list",
            "valid_until",
            "status",
            "is_published",
            "created_at",
        ]

    def get_highlights_list(self, obj):
        return [line.strip() for line in obj.highlights.split("\n") if line.strip()]


class AssociatedCampaignSerializer(serializers.ModelSerializer):
    """Serializer for associated campaigns."""

    class Meta:
        model = AssociatedCampaign
        fields = [
            "id",
            "category",
            "title",
            "description",
            "badge",
            "status",
            "valid_until",
            "is_published",
            "created_at",
        ]


class StatSerializer(serializers.ModelSerializer):
    """Serializer for company statistics."""

    class Meta:
        model = Stat
        fields = ["id", "value", "suffix", "label", "order"]


class TrustedPartnerSerializer(serializers.ModelSerializer):
    """Serializer for trusted partners."""

    class Meta:
        model = TrustedPartner
        fields = ["id", "name", "logo", "website", "is_active", "order"]


class ResourceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceItem
        fields = ["id", "resource_type", "slug", "title", "summary", "image", "specifications", "responsibilities", "is_published", "order"]
