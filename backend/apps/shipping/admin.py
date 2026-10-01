"""
Admin configuration for Shipping models.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Package, Shipment, ShipmentStatus, TrackingEvent, TransportMode


class PackageInline(admin.TabularInline):
    model = Package
    extra = 1
    fields = ["package_number", "description", "quantity", "weight_kg", "is_fragile"]


class TrackingEventInline(admin.TabularInline):
    model = TrackingEvent
    extra = 0
    readonly_fields = ["timestamp"]
    fields = ["status", "location", "description", "timestamp"]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        "tracking_number",
        "customer",
        "sender_name",
        "receiver_name",
        "origin_city",
        "destination_city",
        "transport_mode",
        "status",
        "weight_kg",
        "estimated_delivery",
        "created_at",
    ]
    list_filter = ["status", "transport_mode", "is_fragile", "is_insured", "created_at"]
    search_fields = [
        "tracking_number",
        "sender_name",
        "receiver_name",
        "origin_city",
        "destination_city",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["id", "tracking_number", "created_at", "updated_at"]
    inlines = [PackageInline, TrackingEventInline]

    fieldsets = (
        (_("Suivi"), {
            "fields": ("tracking_number", "customer", "status"),
        }),
        (_("Expéditeur"), {
            "fields": ("sender_name", "sender_address", "sender_phone"),
        }),
        (_("Destinataire"), {
            "fields": ("receiver_name", "receiver_address", "receiver_phone"),
        }),
        (_("Transport"), {
            "fields": ("transport_mode", "origin_city", "origin_country", "destination_city", "destination_country"),
        }),
        (_("Dimensions & Poids"), {
            "fields": ("weight_kg", "length_cm", "width_cm", "height_cm"),
        }),
        (_("Dates"), {
            "fields": ("estimated_pickup", "estimated_delivery", "actual_delivery"),
        }),
        (_("Informations supplémentaires"), {
            "fields": ("description", "special_instructions", "is_fragile", "is_insured", "declared_value"),
        }),
        (_("Horodatage"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = ["mark_as_confirmed", "mark_as_in_transit", "mark_as_delivered", "mark_as_cancelled"]

    @admin.action(description=_("Marquer comme Confirmé"))
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status=ShipmentStatus.CONFIRMED)

    @admin.action(description=_("Marquer comme En transit"))
    def mark_as_in_transit(self, request, queryset):
        queryset.update(status=ShipmentStatus.IN_TRANSIT)

    @admin.action(description=_("Marquer comme Livré"))
    def mark_as_delivered(self, request, queryset):
        queryset.update(status=ShipmentStatus.DELIVERED)

    @admin.action(description=_("Marquer comme Annulé"))
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status=ShipmentStatus.CANCELLED)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["package_number", "shipment", "description", "quantity", "weight_kg", "is_fragile"]
    list_filter = ["is_fragile", "created_at"]
    search_fields = ["package_number", "description", "shipment__tracking_number"]
    ordering = ["package_number"]


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ["shipment", "status", "location", "timestamp", "updated_by"]
    list_filter = ["status", "timestamp"]
    search_fields = ["shipment__tracking_number", "location", "description"]
    ordering = ["-timestamp"]
    readonly_fields = ["timestamp"]
