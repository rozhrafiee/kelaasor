from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OnlineClass, ClassMembership
from .serializers import OnlineClassSerializer, ClassMembershipSerializer
from userapp.models import UserProfile  # Adjust this if your UserProfile model location is different


class CreateOnlineClassView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer
    queryset = OnlineClass.objects.all()

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile  # Assuming the `UserProfile` model is linked to `User`
        serializer.save(created_by=user_profile)

    def post(self, request, *args, **kwargs):
        # Perform additional permission checks if needed
        user_profile = request.user.userprofile
        data = request.data
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save(created_by=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOnlineClassesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer
    queryset = OnlineClass.objects.all()

    def list(self, request, *args, **kwargs):
        # Optionally filter based on user or other criteria
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveOnlineClassView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer
    queryset = OnlineClass.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        online_class = self.get_object()
        serializer = self.get_serializer(online_class)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateClassMembershipView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer
    queryset = ClassMembership.objects.all()

    def post(self, request, *args, **kwargs):
        # Retrieve the online class and user information from the request
        data = request.data
        user_profile = request.user.userprofile
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            online_class_id = data.get('online_class')
            role = data.get('role')

            # Perform additional checks
            online_class = get_object_or_404(OnlineClass, id=online_class_id)
            if role not in ['student', 'teacher', 'mentor']:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user_profile=user_profile, online_class=online_class, role=role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
