from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserEmailSerializer,
)

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token, _ = Token.objects.get_or_create(
                user=user
            )

            return Response(
                {
                    "token": token.key,
                    "fullname": user.first_name,
                    "email": user.email,
                    "user_id": user.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(
                username=email,
                password=password
            )

            if user:
                token, _ = Token.objects.get_or_create(
                    user=user
                )

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
                {
                    "error": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Vetëm user të autentikuar

    def get(self, request):
        email = request.query_params.get("email")
        
        # 1. Kontrollo nëse email është dërguar
        if not email:
            return Response(
                {"error": "Email parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Validimi i formatit
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 3. Kontrollo nëse ekziston
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Email not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 4. Kthe user-in (jo vetëm exists)
        serializer = UserEmailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)