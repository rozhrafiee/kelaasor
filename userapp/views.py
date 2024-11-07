from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from userapp.serializers import UserRegisterSerializer, UserProfileUpdateSerializer

# View for registering a new user, where a role (professor, student, or mentor) is selected during registration.
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for updating the user profile, specifically updating the description field.
class UserProfileUpdateView(UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can update their profile
    queryset = User.objects.all()

    def get_object(self):
        # Return the current user's profile based on the authenticated user.
        return self.request.user.userprofile
