"""
Serializers for Shipping models.
"""

from rest_framework import serializers

from .models import Package, Shipment, ShipmentStatus, TrackingEvent, TransportMode


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package model."""

    class Meta:
        model = Package
        fields = [
            "id",
            "package_number",
            "description",
            "quantity",
            "weight_kg",
            "length_cm",
            "width_cm",
            "height_cm",
            "declared_value",
            "is_fragile",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TrackingEventSerializer(serializers.ModelSerializer):
    """Serializer for TrackingEvent model."""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    updated_by_name = serializers.CharField(source="updated_by.full_name", read_only=True)

    class Meta:
        model = TrackingEvent
        fields = [
            "id",
            "status",
            "status_display",
            "location",
            "description",
            "timestamp",
            "updated_by",
            "updated_by_name",
        ]
        read_only_fields = ["id", "timestamp"]


class ShipmentListSerializer(serializers.ModelSerializer):
    """Serializer for listing shipments (minimal fields)."""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    transport_mode_display = serializers.CharField(source="get_transport_mode_display", read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    package_count = serializers.IntegerField(source="packages.count", read_only=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "tracking_number",
            "customer_name",
            "sender_name",
            "receiver_name",
            "origin_city",
            "origin_country",
            "destination_city",
            "destination_country",
            "transport_mode",
            "transport_mode_display",
            "status",
            "status_display",
            "weight_kg",
            "estimated_delivery",
            "package_count",
            "created_at",
        ]


class ShipmentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed shipment view with packages and tracking."""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    transport_mode_display = serializers.CharField(source="get_transport_mode_display", read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    customer_email = serializers.CharField(source="customer.email", read_only=True)
    packages = PackageSerializer(many=True, read_only=True)
    tracking_events = TrackingEventSerializer(many=True, read_only=True)
    dimensions_display = serializers.ReadOnlyField()
    volume_cm3 = serializers.ReadOnlyField()

    class Meta:
        model = Shipment
        fields = [
            "id",
            "tracking_number",
            "customer_name",
            "customer_email",
            "sender_name",
            "sender_address",
            "sender_phone",
            "receiver_name",
            "receiver_address",
            "receiver_phone",
            "transport_mode",
            "transport_mode_display",
            "status",
            "status_display",
            "weight_kg",
            "length_cm",
            "width_cm",
            "height_cm",
            "dimensions_display",
            "volume_cm3",
            "origin_city",
            "origin_country",
            "destination_city",
            "destination_country",
            "estimated_pickup",
            "estimated_delivery",
            "actual_delivery",
            "description",
            "special_instructions",
            "is_fragile",
            "is_insured",
            "declared_value",
            "packages",
            "tracking_events",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "tracking_number", "created_at", "updated_at"]


class ShipmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new shipment."""

    packages = PackageSerializer(many=True, required=False)

    class Meta:
        model = Shipment
        fields = [
            "customer",
            "sender_name",
            "sender_address",
            "sender_phone",
            "receiver_name",
            "receiver_address",
            "receiver_phone",
            "transport_mode",
            "weight_kg",
            "length_cm",
            "width_cm",
            "height_cm",
            "origin_city",
            "origin_country",
            "destination_city",
            "destination_country",
            "estimated_pickup",
            "estimated_delivery",
            "description",
            "special_instructions",
            "is_fragile",
            "is_insured",
            "declared_value",
            "packages",
        ]

    def create(self, validated_data):
        packages_data = validated_data.pop("packages", [])
        # Generate tracking number
        import uuid
        validated_data["tracking_number"] = f"ESC-{uuid.uuid4().hex[:8].upper()}"
        shipment = Shipment.objects.create(**validated_data)
        # Create packages
        for package_data in packages_data:
            Package.objects.create(shipment=shipment, **package_data)
        # Create initial tracking event
        TrackingEvent.objects.create(
            shipment=shipment,
            status=ShipmentStatus.PENDING,
            description="Shipment created",
        )
        return shipment


class ShipmentStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating shipment status."""

    class Meta:
        model = Shipment
        fields = ["status"]

    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get("status", old_status)
        instance.status = new_status
        instance.save()
        # Create tracking event for status change
        TrackingEvent.objects.create(
            shipment=instance,
            status=new_status,
            description=f"Status changed from {old_status} to {new_status}",
        )
        return instance
