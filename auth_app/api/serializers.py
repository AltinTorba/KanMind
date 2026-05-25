# 1. Django
from django.contrib.auth.models import User

# 2. Third-party (DRF)
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration with password validation."""

    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "fullname",
            "email",
            "password",
            "repeated_password"
        ]

    def validate(self, attrs):
        """Validates that passwords match and email is not already registered."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already exists")

        return attrs

    def create(self, validated_data):
        """Creates a new user with the validated data."""
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        user.first_name = validated_data["fullname"]
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login credentials."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserEmailSerializer(serializers.ModelSerializer):
    """Serializer for returning basic user information by email."""

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        """Returns the user's full name, username, or email as fallback."""
        return obj.first_name or obj.username or obj.email