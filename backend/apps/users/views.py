"""
Views for User management.

Provides CRUD operations for users, profile management,
and authentication token handling.
"""

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .permissions import IsAdmin, IsAdminOrSelf
from .serializers import (
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that includes user data in response."""

    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user CRUD operations.

    - Admins can manage all users
    - Users can view and update their own profile
    - Registration is open to anyone
    """

    queryset = User.objects.all().select_related("profile")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["role", "is_active", "is_email_verified"]
    search_fields = ["email", "username", "first_name", "last_name", "phone_number"]
    ordering_fields = ["date_joined", "last_login", "email", "role"]
    ordering = ["-date_joined"]

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "list":
            return UserListSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsAdminOrSelf()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # Non-admins can only see themselves
        if user.role != "admin":
            queryset = queryset.filter(id=user.id)
        return queryset

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request, pk=None):
        """Allow users to change their password."""
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old_password": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get", "put", "patch"], url_path="me")
    def me(self, request):
        """Get or update the current authenticated user's profile."""
        user = request.user

        if request.method == "GET":
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)

        # PUT/PATCH for updating own profile
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user profile management.

    Users can only access their own profile.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicUserView(APIView):
    """
    Public endpoint for open registration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": UserDetailSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
