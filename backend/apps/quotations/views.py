"""
Views for Quotation management.

Provides:
- Public API endpoint for form submission
- Admin API endpoint for managing quotations
- Email notifications on new submission
"""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Quotation
from .serializers import (
    QuotationCreateSerializer,
    QuotationDetailSerializer,
    QuotationUpdateSerializer,
)


class QuotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for quotation management.

    - Public: POST /api/v1/quotations/ (create new quotation)
    - Admin: GET/PUT/PATCH /api/v1/quotations/ (manage quotations)
    """

    queryset = Quotation.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return QuotationCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return QuotationUpdateSerializer
        return QuotationDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Handle new quotation submission with email notification."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quotation = serializer.save()

        # Send email notifications
        self._send_admin_notification(quotation)
        self._send_client_confirmation(quotation)

        return Response(
            {
                "message": "Votre demande de devis a été enregistrée avec succès. Notre équipe vous recontacte rapidement.",
                "quotation_id": str(quotation.id),
            },
            status=status.HTTP_201_CREATED,
        )

    def _send_admin_notification(self, quotation):
        """Send notification email to admin when new quotation is submitted."""
        try:
            subject = f"[ESC] Nouvelle demande de devis - {quotation.full_name}"
            message = render_to_string("quotations/email/admin_notification.txt", {
                "quotation": quotation,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            # Log error but don't break the submission
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send admin notification email: {e}")

    def _send_client_confirmation(self, quotation):
        """Send confirmation email to client."""
        try:
            subject = "[ESC] Votre demande de devis a bien été reçue"
            message = render_to_string("quotations/email/client_confirmation.txt", {
                "quotation": quotation,
            })
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quotation.email],
                fail_silently=True,
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send client confirmation email: {e}")

    @action(detail=True, methods=["post"], url_path="update-status")
    def update_status(self, request, pk=None):
        """Update quotation status (admin only)."""
        quotation = self.get_object()
        serializer = QuotationUpdateSerializer(quotation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
