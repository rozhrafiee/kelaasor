from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

# Serializer for user registration, validating and creating the User and UserProfile.
class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)  # Password confirmation field
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)  # Field to select user role
    description = serializers.CharField(required=False)  # Optional field for description

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'email', 'role', 'description']  # Fields for registration
        extra_kwargs = {'password': {'write_only': True}}  # Password should not be readable

    # Validate if the passwords match.
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    # Create user and user profile with the provided data.
    def create(self, validated_data):
        # Check if username or email already exists
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError('Email already exists')

        # Create the user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create the user profile with role and description
        user_profile = UserProfile.objects.create(
            user=user,
            role=validated_data['role'],
            description=validated_data.get('description', '')  # If no description provided, use empty string
        )

        return user

# Serializer for updating the user profile, allowing the user to update description.
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['description']  # Allow updating the description field only

