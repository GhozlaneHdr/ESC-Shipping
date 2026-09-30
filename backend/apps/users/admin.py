"""
Admin configuration for user management.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_email_verified",
        "date_joined",
    ]
    list_filter = ["role", "is_active", "is_email_verified", "is_staff", "date_joined"]
    search_fields = ["email", "username", "first_name", "last_name", "phone_number"]
    ordering = ["-date_joined"]
    inlines = [UserProfileInline]

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "avatar", "date_of_birth")}),
        (_("Role"), {"fields": ("role", "is_email_verified", "is_phone_verified")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "last_activity")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "first_name", "last_name", "role", "password1", "password2"),
            },
        ),
    )
