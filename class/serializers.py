from rest_framework import serializers
from .models import OnlineClass, ClassMembership
from userapp.models import UserProfile

class OnlineClassSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating an OnlineClass."""
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OnlineClass
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'code', 'created_by']
        read_only_fields = ['id', 'created_by']
    

class UpdateClassSerializer(serializers.ModelSerializer):
    """Serializer for updating an OnlineClass."""
    class Meta:
        model = OnlineClass
        fields = ['title', 'description', 'start_date', 'end_date']
    

class ClassMemberSerializer(serializers.ModelSerializer):
    """Serializer for displaying members (students, mentors, teachers) of a class."""
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = ClassMembership
        fields = ['username', 'role']


class AddUserToClassSerializer(serializers.Serializer):
    """Serializer for adding users to a class with a specified role."""
    code = serializers.CharField()
    username = serializers.CharField()

    def validate(self, data):
        # Validate class existence
        code = data.get('code')
        username = data.get('username')

        try:
            data['online_class'] = OnlineClass.objects.get(code=code)
        except OnlineClass.DoesNotExist:
            raise serializers.ValidationError("Class with this code does not exist.")

        try:
            data['user_profile'] = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")

        return data

    def create(self, validated_data):
        # Add user to class with specified role
        online_class = validated_data['online_class']
        user_profile = validated_data['user_profile']
        role = validated_data.get('role')

        membership, created = ClassMembership.objects.get_or_create(
            online_class=online_class,
            user_profile=user_profile,
            defaults={'role': role}
        )

        if not created and membership.role != role:
            membership.role = role
            membership.save()

        return membership


class RemoveUserFromClassSerializer(serializers.Serializer):
    """Serializer for removing users from a class based on username and code."""
    code = serializers.CharField()
    username = serializers.CharField()

    def validate(self, data):
        # Validate class existence
        code = data.get('code')
        username = data.get('username')

        try:
            data['online_class'] = OnlineClass.objects.get(code=code)
        except OnlineClass.DoesNotExist:
            raise serializers.ValidationError("Class with this code does not exist.")

        try:
            data['user_profile'] = UserProfile.objects.get(user__username=username)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")

        return data

    def delete(self, validated_data):
        # Remove user from class
        online_class = validated_data['online_class']
        user_profile = validated_data['user_profile']

        membership = ClassMembership.objects.filter(
            online_class=online_class,
            user_profile=user_profile
        ).first()

        if membership:
            membership.delete()
            return True
        return False
