from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import (
    LoginSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

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