"""
Views for Devis management.

Provides:
- Public API endpoint for form submission
- Admin API endpoint for managing devis
- Email notifications on new submission
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Devis
from .serializers import DevisCreateSerializer, DevisDetailSerializer, DevisUpdateSerializer


class DevisViewSet(viewsets.ModelViewSet):
    """
    ViewSet for devis management.

    - Public: POST /api/v1/devis/ (create new devis)
    - Admin: GET/PUT/PATCH /api/v1/devis/ (manage devis)
    """

    queryset = Devis.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return DevisCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return DevisUpdateSerializer
        return DevisDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Handle new devis submission with email notification."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        devis = serializer.save()

        # Send email notifications
        self._send_admin_notification(devis)
        self._send_client_confirmation(devis)

        return Response(
            {
                "message": "Votre demande de devis a été enregistrée avec succès. Notre équipe vous recontacte rapidement.",
                "devis_id": str(devis.id),
            },
            status=status.HTTP_201_CREATED,
        )

    def _send_admin_notification(self, devis):
        """Send notification email to admin when new devis is submitted."""
        try:
            subject = f"[ESC] Nouvelle demande de devis - {devis.full_name}"
            message = render_to_string("devis/email/admin_notification.txt", {
                "devis": devis,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send admin notification email: {e}")

    def _send_client_confirmation(self, devis):
        """Send confirmation email to client."""
        try:
            subject = "[ESC] Votre demande de devis a bien été reçue"
            message = render_to_string("devis/email/client_confirmation.txt", {
                "devis": devis,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[devis.email],
                fail_silently=True,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send client confirmation email: {e}")

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        """Update devis status (admin only)."""
        devis = self.get_object()
        serializer = DevisUpdateSerializer(devis, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
