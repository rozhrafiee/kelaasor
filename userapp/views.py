from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserChangePasswordSerializer, UserProfileUpdateSerializer
from rest_framework.exceptions import ValidationError
from .models import UserProfile

class Login(TokenObtainPairView):
    pass

class Refresh(TokenRefreshView):
    pass

class Register(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "You registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserProfileUpdateSerializer(user.userprofile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, username):
        try:
            user = User.objects.get(username=username)
            profile = user.userprofile
            serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ChangePasswordView(APIView):
    def patch(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = UserChangePasswordSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
