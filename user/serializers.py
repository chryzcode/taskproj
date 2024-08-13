from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Excludes the password field and makes certain fields read-only.
    """
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ('id', 'is_active', 'is_staff', 'created', 'updated')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles the creation of a new user with the provided email, full name, and password.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates the user's email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
