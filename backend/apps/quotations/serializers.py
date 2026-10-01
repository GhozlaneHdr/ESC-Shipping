"""
Serializers for Quotation model.
"""

from rest_framework import serializers

from .models import Quotation, QuotationStatus


class QuotationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new quotation request.
    Used by the public API endpoint.
    """

    class Meta:
        model = Quotation
        fields = [
            "full_name",
            "company",
            "email",
            "phone",
            "service_type",
            "departure",
            "destination",
            "message",
        ]

    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value.strip()

    def validate_phone(self, value):
        if len(value.strip()) < 6:
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value.strip()

    def validate_service_type(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Please select a service type.")
        return value.strip()

    def validate_departure(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Please enter a departure location.")
        return value.strip()

    def validate_destination(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Please enter a destination.")
        return value.strip()


class QuotationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed quotation view (admin use).
    """

    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Quotation
        fields = [
            "id",
            "full_name",
            "company",
            "email",
            "phone",
            "service_type",
            "departure",
            "destination",
            "message",
            "status",
            "status_display",
            "admin_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]


class QuotationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating quotation status (admin use).
    """

    class Meta:
        model = Quotation
        fields = ["status", "admin_notes"]
