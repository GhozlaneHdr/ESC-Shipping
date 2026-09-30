from rest_framework import serializers
from .models import (
    MaritimeCampaign,
    AssociatedCampaign,
    Service,
    ServiceStep,
    Stat,
    TrustedPartner,
)

class MaritimeCampaignSerializer(serializers.ModelSerializer):
    highlights_list = serializers.ListField(
        child=serializers.CharField(), source="get_highlights_list", read_only=True
    )

    class Meta:
        model = MaritimeCampaign
        fields = [
            "id",
            "title",
            "subtitle",
            "description",
            "route_from",
            "route_to",
            "discount",
            "status",
            "valid_until",
            "highlights_list",
        ]

class AssociatedCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociatedCampaign
        fields = [
            "id",
            "title",
            "category",
            "description",
            "badge",
            "status",
            "valid_until",
        ]

class ServiceStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceStep
        fields = ["title", "text", "order"]

class ServiceSerializer(serializers.ModelSerializer):
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
            "benefits_list",
            "why_us_list",
            "steps",
        ]

    def get_benefits_list(self, obj):
        return [line.strip() for line in obj.benefits.strip().split("\n") if line.strip()]

    def get_why_us_list(self, obj):
        return [line.strip() for line in obj.why_us.strip().split("\n") if line.strip()]

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ["value", "suffix", "label"]

class TrustedPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustedPartner
        fields = ["id", "name", "logo", "website"]
