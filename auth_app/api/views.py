# 1. Django
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# 2. Third-party (DRF)
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Local imports
from auth_app.api.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserEmailSerializer,
)


class RegisterView(APIView):
    """Handles user registration and token generation."""

    permission_classes = []

    def post(self, request):
        """Creates a new user and returns a token with user information."""
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "token": token.key,
                    "fullname": user.first_name,
                    "email": user.email,
                    "user_id": user.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Handles user authentication and token retrieval."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticates a user and returns a token with user information."""
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(username=email, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "token": token.key,
                        "fullname": user.first_name,
                        "email": user.email,
                        "user_id": user.id
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """Handles email existence check for registered users."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns user data if the given email exists in the system."""
        email = request.query_params.get("email")

        if not email:
            return Response(
                {"error": "Email parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Email not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserEmailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)