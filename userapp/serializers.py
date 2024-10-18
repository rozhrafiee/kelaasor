from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirmation', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        # At this point, `password_confirmation` is already removed by the `validate` method
        role = self.context['request'].data.get('role')  # Grab role from the request data
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create associated UserProfile
        UserProfile.objects.create(user=user, role=role)
        return user

class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirmation = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password_confirmation']

    def validate(self, data):
        user = self.instance
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError('Old password is incorrect')

        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError('New passwords do not match')

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['role']
