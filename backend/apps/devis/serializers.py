"""
Serializers for Devis model.
"""

from rest_framework import serializers

from .models import Devis


class DevisCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new devis request.
    Used by the public API endpoint.
    """

    class Meta:
        model = Devis
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
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return value.strip()

    def validate_phone(self, value):
        if len(value.strip()) < 6:
            raise serializers.ValidationError("Veuillez entrer un numéro de téléphone valide.")
        return value.strip()

    def validate_service_type(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Veuillez sélectionner un type de service.")
        return value.strip()

    def validate_departure(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Veuillez indiquer un lieu de départ.")
        return value.strip()

    def validate_destination(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Veuillez indiquer une destination.")
        return value.strip()


class DevisDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed devis view (admin use).
    """

    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Devis
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


class DevisUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating devis status (admin use).
    """

    class Meta:
        model = Devis
        fields = ["status", "admin_notes"]
