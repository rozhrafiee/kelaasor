from rest_framework import serializers
from .models import OnlineClass, ClassMembership


class OnlineClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = '__all__'


from rest_framework import serializers
from .models import ClassMembership, OnlineClass
from userapp.models import UserProfile

class ClassMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMembership
        fields = ['online_class', 'user_profile', 'role']  # Keep the relevant fields here

    def create(self, validated_data):
        # Ensure that these fields are set when creating the membership
        online_class = validated_data.get('online_class')
        user_profile = validated_data.get('user_profile')
        role = validated_data.get('role')

        # Create and return the class membership instance
        membership = ClassMembership.objects.create(
            online_class=online_class,
            user_profile=user_profile,
            role=role
        )
        return membership


class EnterTheClassByPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
