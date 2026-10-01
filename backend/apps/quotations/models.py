"""
Quotation model for ESC Shipping.

Stores quote requests submitted through the front-end form.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class QuotationStatus(models.TextChoices):
    """Status choices for quotation requests."""

    NEW = "new", _("New")
    IN_REVIEW = "in_review", _("In Review")
    QUOTED = "quoted", _("Quoted")
    ACCEPTED = "accepted", _("Accepted")
    REJECTED = "rejected", _("Rejected")
    ARCHIVED = "archived", _("Archived")


class Quotation(models.Model):
    """
    Quote request from a potential client.

    Stores contact information, service details, and message
    from the quotation form on the front-end.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    # Client Information
    full_name = models.CharField(
        max_length=150,
        verbose_name=_("Full Name"),
        help_text=_("Client's full name."),
    )
    company = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Company"),
        help_text=_("Company name (optional)."),
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        help_text=_("Client's email address."),
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone"),
        help_text=_("Client's phone number."),
    )
    # Service Details
    service_type = models.CharField(
        max_length=100,
        verbose_name=_("Service Type"),
        help_text=_("Type of service requested."),
    )
    departure = models.CharField(
        max_length=150,
        verbose_name=_("Departure"),
        help_text=_("City or country of departure."),
    )
    destination = models.CharField(
        max_length=150,
        verbose_name=_("Destination"),
        help_text=_("City or country of destination."),
    )
    message = models.TextField(
        blank=True,
        verbose_name=_("Message"),
        help_text=_("Additional details about the shipment."),
    )
    # Status & Tracking
    status = models.CharField(
        max_length=20,
        choices=QuotationStatus.choices,
        default=QuotationStatus.NEW,
        db_index=True,
        verbose_name=_("Status"),
        help_text=_("Current status of the quotation request."),
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name=_("Admin Notes"),
        help_text=_("Internal notes (not visible to client)."),
    )
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("Created At"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )

    class Meta:
        verbose_name = _("Quotation")
        verbose_name_plural = _("Quotations")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"], name="quotation_status_created_idx"),
            models.Index(fields=["email"], name="quotation_email_idx"),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.service_type} ({self.status})"
