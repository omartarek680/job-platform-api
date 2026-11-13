from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def validate_first_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "First name should be at least 3 characters"
            )
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "First name must contain only letters, and spaces."
            )

        return value.title()

    def validate_last_name(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "Last name should be at least 3 characters"
            )
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "Last name must contain only letters, and spaces."
            )
        return value.title()

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError("Passwords must match")

        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password", None)
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "re_password",
            "role",
        ]
