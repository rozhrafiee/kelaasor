from rest_framework import serializers
from .models import OnlineClass, ClassMembership


class OnlineClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = '__all__'


class ClassMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMembership
        fields = '__all__'
