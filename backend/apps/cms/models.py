import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class CampaignStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    LIMITED = "limited", _("Limited Offer")
    UPCOMING = "upcoming", _("Upcoming")
    EXPIRED = "expired", _("Expired")

class BaseCampaign(models.Model):
    """Abstract base model for shared campaign fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text=_("Main title of the campaign."))
    description = models.TextField(help_text=_("Detailed description of the offer."))
    status = models.CharField(max_length=20, choices=CampaignStatus.choices, default=CampaignStatus.ACTIVE)
    valid_until = models.DateField(help_text=_("Expiration date for the offer."))
    is_published = models.BooleanField(default=True, help_text=_("Toggle to hide/show on website."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MaritimeCampaign(BaseCampaign):
    """Specific model for Maritime shipping campaigns."""
    subtitle = models.CharField(max_length=200, help_text=_("Subtitle (e.g., Ligne Europe - Algérie)"))
    route_from = models.CharField(max_length=150, help_text=_("Departure point (e.g., Marseille / Gênes)"))
    route_to = models.CharField(max_length=150, help_text=_("Arrival point (e.g., Alger / Béjaïa)"))
    discount = models.CharField(max_length=50, help_text=_("Discount text (e.g., '-15%')"))
    
    # Store highlights as a simple text block, one per line, or JSON.
    highlights = models.TextField(help_text=_("List of bullet points. Enter one per line."))

    class Meta:
        verbose_name = _("Maritime Campaign")
        verbose_name_plural = _("Maritime Campaigns")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.discount})"
        
    def get_highlights_list(self):
        return [line.strip() for line in self.highlights.strip().split('\n') if line.strip()]

class AssociatedCampaign(BaseCampaign):
    """Model for associated campaigns/bundles (e.g., Port Logistics)."""
    category = models.CharField(max_length=100, help_text=_("Category (e.g., Logistique portuaire)"))
    badge = models.CharField(max_length=50, help_text=_("Badge text (e.g., Bundle, Nouveau)"))

    class Meta:
        verbose_name = _("Associated Campaign")
        verbose_name_plural = _("Associated Campaigns")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.category}: {self.title}"

class Service(models.Model):
    """Core shipping services (Maritime, Air, Road, etc.)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, help_text=_("URL slug for the service."))
    name = models.CharField(max_length=100)
    short_description = models.TextField(help_text=_("Brief description for cards."))
    long_intro = models.TextField(help_text=_("Introduction text on detail page."))
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    
    # Storing lists as line-break separated text for simple DB entry via Admin
    benefits = models.TextField(help_text=_("One benefit per line."))
    why_us = models.TextField(help_text=_("One reason per line."))
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text=_("Display order priority."))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class SiteBranding(models.Model):
    """Admin-managed brand assets used throughout the website."""
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    logo = models.ImageField(upload_to="branding/")
    hero_video = models.FileField(
        upload_to="branding/",
        blank=True,
        null=True,
        help_text="Optional looping video for the homepage hero background.",
    )

    class Meta:
        verbose_name = "Site branding"
        verbose_name_plural = "Site branding"

    def __str__(self):
        return "ESC site branding"

class ServiceStep(models.Model):
    """Steps involved in a specific service."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField(max_length=150)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Service Step")
        verbose_name_plural = _("Service Steps")
        ordering = ["order"]

    def __str__(self):
        return f"{self.service.name} - Step: {self.title}"

class Stat(models.Model):
    """Company statistics shown on homepage."""
    value = models.IntegerField()
    suffix = models.CharField(max_length=10, blank=True, help_text=_("e.g. '+' or '%'"))
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Statistic")
        verbose_name_plural = _("Statistics")
        ordering = ["order"]

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"

class TrustedPartner(models.Model):
    """Trusted partners to display in the marquee."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="partners/")
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Trusted Partner")
        verbose_name_plural = _("Trusted Partners")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
