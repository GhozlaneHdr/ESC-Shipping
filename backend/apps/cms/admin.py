from django.contrib import admin
from .models import AssociatedCampaign, MaritimeCampaign, Service, ServiceStep, SiteBranding, Stat, TrustedPartner

@admin.register(MaritimeCampaign)
class MaritimeCampaignAdmin(admin.ModelAdmin):
    list_display = ["title", "route_from", "route_to", "discount", "status", "valid_until", "is_published"]
    list_filter = ["status", "is_published"]
    search_fields = ["title", "subtitle", "route_from", "route_to"]
    ordering = ["-created_at"]

@admin.register(AssociatedCampaign)
class AssociatedCampaignAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "badge", "status", "valid_until", "is_published"]
    list_filter = ["status", "category", "is_published"]
    search_fields = ["title", "category"]
    ordering = ["-created_at"]

class ServiceStepInline(admin.StackedInline):
    model = ServiceStep
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_active", "order"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ServiceStepInline]
    ordering = ["order", "name"]


@admin.register(SiteBranding)
class SiteBrandingAdmin(admin.ModelAdmin):
    list_display = ["__str__", "logo", "hero_video"]

    def has_add_permission(self, request):
        return not SiteBranding.objects.exists()

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ["label", "value", "suffix", "order"]
    list_editable = ["value", "suffix", "order"]
    ordering = ["order"]

@admin.register(TrustedPartner)
class TrustedPartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "order"]
    list_editable = ["order", "is_active"]
    search_fields = ["name"]
    ordering = ["order", "name"]
