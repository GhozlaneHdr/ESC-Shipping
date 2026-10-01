"""
Fix or create the admin user for Django admin access.

Usage:
    python manage.py fix_admin
"""

from django.core.management.base import BaseCommand
from apps.users.models import User, UserRole


class Command(BaseCommand):
    help = "Create or fix the admin user for Django admin access."

    def handle(self, *args, **options):
        email = "admin@esc-shipping.com"
        password = "admin123"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": "admin",
                "first_name": "Admin",
                "last_name": "ESC",
                "role": UserRole.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user: {email}"))
        else:
            # Ensure admin permissions are correct
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.role = UserRole.ADMIN
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Fixed admin user: {email}"))

        self.stdout.write(f"  Email: {user.email}")
        self.stdout.write(f"  Staff: {user.is_staff}")
        self.stdout.write(f"  Superuser: {user.is_superuser}")
        self.stdout.write(f"  Active: {user.is_active}")
        self.stdout.write(f"  Password: {password}")
