"""
URL configuration for Quotation management.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import QuotationViewSet

router = DefaultRouter()
router.register(r"quotations", QuotationViewSet, basename="quotation")

urlpatterns = [
    path("", include(router.urls)),
]
