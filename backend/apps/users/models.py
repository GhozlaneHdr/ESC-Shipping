"""
User models for ESC Shipping.

Extends Django's AbstractUser with a custom User model and UserProfile
for role-based access and extended user information.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    """Predefined user roles for the shipping platform."""

    ADMIN = "admin", _("Admin")
    MANAGER = "manager", _("Manager")
    CLIENT = "client", _("Client")
    DRIVER = "driver", _("Driver")
    WAREHOUSE_STAFF = "warehouse_staff", _("Warehouse Staff")
    SUPPORT = "support", _("Support Agent")


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.

    Adds role-based access control, email as unique identifier,
    phone number support, and UUID public identifier for API exposure.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Public identifier exposed in the API."),
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        },
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message=_("Phone number must be entered in format: '+999999999' (up to 15 digits)."),
            )
        ],
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        db_index=True,
        help_text=_("Determines user permissions and dashboard access."),
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as the login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"], name="user_email_idx"),
            models.Index(fields=["role", "is_active"], name="user_role_active_idx"),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_driver(self):
        return self.role == UserRole.DRIVER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_client(self):
        return self.role == UserRole.CLIENT


class UserProfile(models.Model):
    """
    Extended profile information for users.

    Stores additional details that don't belong on the core User model,
    such as address, preferences, and role-specific metadata.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    # Address
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, db_index=True)
    # Company (for business clients and staff)
    company_name = models.CharField(max_length=255, blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    # Driver-specific
    license_number = models.CharField(max_length=100, blank=True)
    license_expiry = models.DateField(null=True, blank=True)
    # Preferences
    preferred_language = models.CharField(max_length=10, default="en")
    timezone = models.CharField(max_length=50, default="UTC")
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Profile of {self.user.email}"
