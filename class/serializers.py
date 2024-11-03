from rest_framework import serializers
from .models import OnlineClass, ClassMembership

class OnlineClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'created_by']

class ClassMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMembership
        fields = ['id', 'user_profile', 'online_class', 'role']
