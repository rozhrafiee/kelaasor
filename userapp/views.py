from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserProfileSerializer
from .models import UserProfile

class Register(APIView):
    def post(self, request):
        user_serializer = UserRegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            role = request.data.get('role')  # Get the role from the request data
            UserProfile.objects.create(user=user, role=role)  # Create UserProfile
            return Response({"message": "You registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate tokens or return user details as needed
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class ChangePassword(APIView):
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
