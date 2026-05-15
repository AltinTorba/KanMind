from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        fullname = validated_data["fullname"]
        password = validated_data["password"]

        user = User(
            username=fullname,
            email=validated_data["email"]
        )

        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)