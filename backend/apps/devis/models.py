"""
Devis model for ESC Shipping.

Stores quote requests submitted through the front-end form.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class DevisStatus(models.TextChoices):
    """Status choices for devis requests."""

    NEW = "new", _("Nouveau")
    IN_REVIEW = "in_review", _("En cours d'étude")
    QUOTED = "quoted", _("Devis envoyé")
    ACCEPTED = "accepted", _("Accepté")
    REJECTED = "rejected", _("Refusé")
    ARCHIVED = "archived", _("Archivé")


class Devis(models.Model):
    """
    Devis (quote request) from a potential client.

    Stores contact information, service details, and message
    from the devis form on the front-end.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # Client Information
    full_name = models.CharField(
        max_length=150,
        verbose_name=_("Nom complet"),
        help_text=_("Nom complet du client."),
    )
    company = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Société"),
        help_text=_("Nom de la société (optionnel)."),
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("Adresse email du client."),
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Téléphone"),
        help_text=_("Numéro de téléphone du client."),
    )
    # Service Details
    service_type = models.CharField(
        max_length=100,
        verbose_name=_("Type de service"),
        help_text=_("Type de service demandé."),
    )
    departure = models.CharField(
        max_length=150,
        verbose_name=_("Départ"),
        help_text=_("Ville ou pays de départ."),
    )
    destination = models.CharField(
        max_length=150,
        verbose_name=_("Destination"),
        help_text=_("Ville ou pays de destination."),
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("Message"),
        help_text=_("Détails supplémentaires sur l'expédition."),
    )
    # Status & Tracking
    status = models.CharField(
        max_length=20,
        choices=DevisStatus.choices,
        default=DevisStatus.NEW,
        db_index=True,
        verbose_name=_("Statut"),
        help_text=_("Statut actuel de la demande de devis."),
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name=_("Notes admin"),
        help_text=_("Notes internes (non visibles par le client)."),
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
        verbose_name = _("Devis")
        verbose_name_plural = _("Devis")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="devis_status_created_idx"),
            models.Index(fields=["email"], name="devis_email_idx"),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.service_type} ({self.status})"
