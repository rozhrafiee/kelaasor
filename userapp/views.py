from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .models import UserProfile
from .serializers import UserProfileSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile


