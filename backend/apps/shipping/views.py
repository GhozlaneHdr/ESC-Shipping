"""
Views for Shipping management.

Provides CRUD operations for shipments, packages, and tracking events.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Package, Shipment, ShipmentStatus, TrackingEvent
from .serializers import (
    PackageSerializer,
    ShipmentCreateSerializer,
    ShipmentDetailSerializer,
    ShipmentListSerializer,
    ShipmentStatusUpdateSerializer,
    TrackingEventSerializer,
)


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for shipment CRUD operations.

    - List: GET /api/v1/shipping/shipments/
    - Create: POST /api/v1/shipping/shipments/
    - Detail: GET /api/v1/shipping/shipments/{id}/
    - Update: PUT/PATCH /api/v1/shipping/shipments/{id}/
    - Delete: DELETE /api/v1/shipping/shipments/{id}/
    """

    queryset = Shipment.objects.all().prefetch_related("packages", "tracking_events")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "transport_mode", "origin_city", "destination_city", "customer"]
    search_fields = [
        "tracking_number",
        "sender_name",
        "receiver_name",
        "origin_city",
        "destination_city",
        "description",
    ]
    ordering_fields = ["created_at", "estimated_delivery", "weight_kg", "status"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return ShipmentCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ShipmentStatusUpdateSerializer
        elif self.action == "list":
            return ShipmentListSerializer
        return ShipmentDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # Non-admin users can only see their own shipments
        if user.role != "admin":
            queryset = queryset.filter(customer=user)
        return queryset

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        """Update shipment status and create tracking event."""
        shipment = self.get_object()
        serializer = ShipmentStatusUpdateSerializer(shipment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="tracking")
    def tracking(self, request, pk=None):
        """Get tracking history for a shipment."""
        shipment = self.get_object()
        events = shipment.tracking_events.all()
        serializer = TrackingEventSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-tracking-number")
    def by_tracking_number(self, request):
        """Lookup shipment by tracking number (public endpoint)."""
        tracking_number = request.query_params.get("number")
        if not tracking_number:
            return Response(
                {"error": "Tracking number is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
            serializer = ShipmentDetailSerializer(shipment)
            return Response(serializer.data)
        except Shipment.DoesNotExist:
            return Response(
                {"error": "Shipment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PackageViewSet(viewsets.ModelViewSet):
    """ViewSet for package CRUD operations."""

    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["shipment", "is_fragile"]
    search_fields = ["package_number", "description"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role != "admin":
            queryset = queryset.filter(shipment__customer=user)
        return queryset


class TrackingEventViewSet(viewsets.ModelViewSet):
    """ViewSet for tracking event management."""

    queryset = TrackingEvent.objects.all()
    serializer_class = TrackingEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["shipment", "status"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role != "admin":
            queryset = queryset.filter(shipment__customer=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)
