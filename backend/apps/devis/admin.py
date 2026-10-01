"""
Admin configuration for Devis model.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Devis, DevisStatus


@admin.register(Devis)
class DevisAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "company",
        "email",
        "phone",
        "service_type",
        "status",
        "created_at",
    ]
    list_filter = ["status", "service_type", "created_at"]
    search_fields = ["full_name", "company", "email", "phone", "service_type"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = (
        (_("Informations client"), {
            "fields": ("full_name", "company", "email", "phone"),
        }),
        (_("Détails du service"), {
            "fields": ("service_type", "departure", "destination", "message"),
        }),
        (_("Statut"), {
            "fields": ("status", "admin_notes"),
        }),
        (_("Horodatage"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = ["mark_as_in_review", "mark_as_quoted", "mark_as_accepted", "mark_as_rejected"]

    @admin.action(description=_("Marquer comme En cours d'étude"))
    def mark_as_in_review(self, request, queryset):
        queryset.update(status=DevisStatus.IN_REVIEW)

    @admin.action(description=_("Marquer comme Devis envoyé"))
    def mark_as_quoted(self, request, queryset):
        queryset.update(status=DevisStatus.QUOTED)

    @admin.action(description=_("Marquer comme Accepté"))
    def mark_as_accepted(self, request, queryset):
        queryset.update(status=DevisStatus.ACCEPTED)

    @admin.action(description=_("Marquer comme Refusé"))
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=DevisStatus.REJECTED)
