"""
Shipping models for ESC Shipping.

Manages shipments, packages, and tracking events.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class ShipmentStatus(models.TextChoices):
    """Status choices for shipments."""

    PENDING = "pending", _("En attente")
    CONFIRMED = "confirmed", _("Confirmé")
    PICKED_UP = "picked_up", _("Ramassé")
    IN_TRANSIT = "in_transit", _("En transit")
    AT_WAREHOUSE = "at_warehouse", _("À l'entrepôt")
    OUT_FOR_DELIVERY = "out_for_delivery", _("En livraison")
    DELIVERED = "delivered", _("Livré")
    CANCELLED = "cancelled", _("Annulé")
    EXCEPTION = "exception", _("Exception")


class TransportMode(models.TextChoices):
    """Transport mode choices."""

    SEA = "sea", _("Maritime")
    AIR = "air", _("Aérien")
    ROAD = "road", _("Routier")
    RAIL = "rail", _("Ferroviaire")


class Shipment(models.Model):
    """
    Shipment model representing a single shipment/order.

    Contains all details about a shipment including origin, destination,
    transport mode, dimensions, and current status.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    tracking_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name=_("Numéro de suivi"),
        help_text=_("Unique tracking number for the shipment."),
    )
    # Relationships
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="shipments",
        verbose_name=_("Client"),
        help_text=_("Customer who owns this shipment."),
    )
    sender_name = models.CharField(
        max_length=150,
        verbose_name=_("Nom de l'expéditeur"),
    )
    sender_address = models.TextField(
        verbose_name=_("Adresse de l'expéditeur"),
    )
    sender_phone = models.CharField(
        max_length=20,
        verbose_name=_("Téléphone de l'expéditeur"),
    )
    receiver_name = models.CharField(
        max_length=150,
        verbose_name=_("Nom du destinataire"),
    )
    receiver_address = models.TextField(
        verbose_name=_("Adresse du destinataire"),
    )
    receiver_phone = models.CharField(
        max_length=20,
        verbose_name=_("Téléphone du destinataire"),
    )
    # Shipment Details
    transport_mode = models.CharField(
        max_length=20,
        choices=TransportMode.choices,
        default=TransportMode.SEA,
        db_index=True,
        verbose_name=_("Mode de transport"),
    )
    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING,
        db_index=True,
        verbose_name=_("Statut"),
    )
    # Dimensions & Weight
    weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Poids (kg)"),
    )
    length_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Longueur (cm)"),
    )
    width_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Largeur (cm)"),
    )
    height_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Hauteur (cm)"),
    )
    # Locations
    origin_city = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Ville d'origine"),
    )
    origin_country = models.CharField(
        max_length=100,
        verbose_name=_("Pays d'origine"),
    )
    destination_city = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Ville de destination"),
    )
    destination_country = models.CharField(
        max_length=100,
        verbose_name=_("Pays de destination"),
    )
    # Dates
    estimated_pickup = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de ramassage estimée"),
    )
    estimated_delivery = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de livraison estimée"),
    )
    actual_delivery = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date de livraison réelle"),
    )
    # Additional Info
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )
    special_instructions = models.TextField(
        blank=True,
        verbose_name=_("Instructions spéciales"),
    )
    is_fragile = models.BooleanField(
        default=False,
        verbose_name=_("Fragile"),
    )
    is_insured = models.BooleanField(
        default=False,
        verbose_name=_("Assuré"),
    )
    declared_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Valeur déclarée"),
    )
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Créé le"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Mis à jour le"),
    )

    class Meta:
        verbose_name = _("Expédition")
        verbose_name_plural = _("Expéditions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="shipment_status_created_idx"),
            models.Index(fields=["customer", "status"], name="shipment_customer_status_idx"),
            models.Index(fields=["origin_city", "destination_city"], name="shipment_route_idx"),
        ]

    def __str__(self):
        return f"{self.tracking_number} - {self.sender_name} → {self.receiver_name}"

    @property
    def volume_cm3(self):
        """Calculate volume in cubic centimeters."""
        if self.length_cm and self.width_cm and self.height_cm:
            return self.length_cm * self.width_cm * self.height_cm
        return None

    @property
    def dimensions_display(self):
        """Return formatted dimensions string."""
        if self.length_cm and self.width_cm and self.height_cm:
            return f"{self.length_cm} × {self.width_cm} × {self.height_cm} cm"
        return "N/A"


class Package(models.Model):
    """
    Package model representing individual items within a shipment.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="packages",
        verbose_name=_("Expédition"),
    )
    package_number = models.CharField(
        max_length=50,
        verbose_name=_("Numéro de colis"),
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Description"),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité"),
    )
    weight_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Poids (kg)"),
    )
    length_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Longueur (cm)"),
    )
    width_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Largeur (cm)"),
    )
    height_cm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Hauteur (cm)"),
    )
    declared_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Valeur déclarée"),
    )
    is_fragile = models.BooleanField(
        default=False,
        verbose_name=_("Fragile"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Créé le"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Mis à jour le"),
    )

    class Meta:
        verbose_name = _("Colis")
        verbose_name_plural = _("Colis")
        ordering = ["package_number"]
        unique_together = ["shipment", "package_number"]

    def __str__(self):
        return f"{self.package_number} - {self.description or 'Colis'}"


class TrackingEvent(models.Model):
    """
    Tracking event model for shipment status history.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name="tracking_events",
        verbose_name=_("Expédition"),
    )
    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        verbose_name=_("Statut"),
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Lieu"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Horodatage"),
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracking_events",
        verbose_name=_("Mis à jour par"),
    )

    class Meta:
        verbose_name = _("Événement de suivi")
        verbose_name_plural = _("Événements de suivi")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.get_status_display()} - {self.timestamp}"
