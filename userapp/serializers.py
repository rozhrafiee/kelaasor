from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create the User instance
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()

        # Check if the user already has a profile, if not, create one
        if not UserProfile.objects.filter(user=user).exists():
            UserProfile.objects.create(user=user)
        
        return user
