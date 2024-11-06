from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import OnlineClass, ClassMembership
from .serializers import OnlineClassSerializer, ClassMembershipSerializer
from userapp.models import UserProfile  # Adjust if your UserProfile model location is different

# View for creating an online class
class CreateOnlineClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer
    queryset = OnlineClass.objects.all()

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        serializer.save(created_by=user_profile)

# View for updating an online class
class UpdateOnlineClass(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer
    queryset = OnlineClass.objects.all()
    lookup_field = 'pk'

# View for adding a mentor to a class
class AddMentorToClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer
    queryset = ClassMembership.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        user_profile = request.user.userprofile
        online_class_id = data.get('online_class')
        role = 'mentor'  # Specific role for this view

        online_class = get_object_or_404(OnlineClass, id=online_class_id)
        serializer = self.get_serializer(data={'online_class': online_class_id, 'role': role, 'user_profile': user_profile.id})

        if serializer.is_valid():
            serializer.save(user_profile=user_profile, online_class=online_class, role=role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for viewing students in a class
class OnlineClassViewStudentsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def get_queryset(self):
        return ClassMembership.objects.filter(online_class_id=self.kwargs['pk'], role='student')

# View for adding a teacher to a class
class AddTeacherToClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user_profile = request.user.userprofile
        online_class_id = data.get('online_class')
        role = 'teacher'

        online_class = get_object_or_404(OnlineClass, id=online_class_id)
        serializer = self.get_serializer(data={'online_class': online_class_id, 'role': role, 'user_profile': user_profile.id})

        if serializer.is_valid():
            serializer.save(user_profile=user_profile, online_class=online_class, role=role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for removing a student from a class
class RemoveStudentFromClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        online_class_id = data.get('online_class')
        student_id = data.get('student_id')

        membership = get_object_or_404(ClassMembership, online_class_id=online_class_id, user_profile_id=student_id, role='student')
        membership.delete()
        return Response({"detail": "Student removed from class"}, status=status.HTTP_204_NO_CONTENT)

# View for entering a class by password
class EnterTheClassByPasswordView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        class_id = request.data.get('class_id')
        online_class = get_object_or_404(OnlineClass, id=class_id, password=password)

        # Add user to class if authenticated and password is correct
        return Response(self.get_serializer(online_class).data, status=status.HTTP_200_OK)

# View for sending an invite to a class
class SendInviteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

# View for confirming enrollment in a class
class ConfirmEnrollmentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

# View for students to view their classes
class StudentClassView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def get_queryset(self):
        return ClassMembership.objects.filter(user_profile=self.request.user.userprofile, role='student')

# View for adding a student to a class
class StudentAddView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer
