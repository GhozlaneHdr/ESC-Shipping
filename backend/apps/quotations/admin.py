"""
Admin configuration for Quotation model.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Quotation, QuotationStatus


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
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
        (_("Client Information"), {
            "fields": ("full_name", "company", "email", "phone"),
        }),
        (_("Service Details"), {
            "fields": ("service_type", "departure", "destination", "message"),
        }),
        (_("Status"), {
            "fields": ("status", "admin_notes"),
        }),
        (_("Timestamps"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    actions = ["mark_as_in_review", "mark_as_quoted", "mark_as_accepted", "mark_as_rejected"]

    @admin.action(description=_("Mark selected quotations as In Review"))
    def mark_as_in_review(self, request, queryset):
        queryset.update(status=QuotationStatus.IN_REVIEW)

    @admin.action(description=_("Mark selected quotations as Quoted"))
    def mark_as_quoted(self, request, queryset):
        queryset.update(status=QuotationStatus.QUOTED)

    @admin.action(description=_("Mark selected quotations as Accepted"))
    def mark_as_accepted(self, request, queryset):
        queryset.update(status=QuotationStatus.ACCEPTED)

    @admin.action(description=_("Mark selected quotations as Rejected"))
    def mark_as_rejected(self, request, queryset):
        queryset.update(status=QuotationStatus.REJECTED)
