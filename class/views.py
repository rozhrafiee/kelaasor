from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .models import OnlineClass, ClassMembership
from userapp.models import UserProfile
from .serializers import OnlineClassSerializer, ClassMembershipSerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User
class CreateOnlineClass(CreateAPIView):
    serializer_class = OnlineClassSerializer

    def create(self, request, *args, **kwargs):
        # Get the professor by username (you can also use 'name' or 'email')
        professor_username = request.data.get('professor_username')
        try:
            professor = User.objects.get(username=professor_username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Professor not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the class with the professor as the creator
        new_class = OnlineClass.objects.create(
            title=request.data['title'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            created_by=professor.userprofile,  # Assuming UserProfile is linked to User
        )

        # Serialize and return the class details in the response
        return Response(
            {"message": "Class created successfully", "class": OnlineClassSerializer(new_class).data},
            status=status.HTTP_201_CREATED
        )


class UpdateOnlineClass(UpdateAPIView):
    """Updates an existing online class."""
    permission_classes = [IsAuthenticated]
    queryset = OnlineClass.objects.all()
    serializer_class = OnlineClassSerializer

    def perform_update(self, serializer):
        online_class = self.get_object()
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        serializer.save()


class ListOnlineClasses(ListAPIView):
    """Lists all classes the user is enrolled in."""
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer

    def get_queryset(self):
        return OnlineClass.objects.filter(students=self.request.user.userprofile)


class RetrieveOnlineClass(RetrieveAPIView):
    """Retrieve details of a single class."""
    permission_classes = [IsAuthenticated]
    queryset = OnlineClass.objects.all()
    serializer_class = OnlineClassSerializer


class AddMentorToClass(CreateAPIView):
    """Adds a mentor to a class."""
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        
        mentor = get_object_or_404(UserProfile, id=self.request.data['mentor_id'])
        serializer.save(online_class=online_class, user_profile=mentor, role='mentor')


class AddTeacherToClass(CreateAPIView):
    """Adds a teacher to a class."""
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        
        teacher = get_object_or_404(UserProfile, id=self.request.data['teacher_id'])
        serializer.save(online_class=online_class, user_profile=teacher, role='professor')

class AddStudentToClass(CreateAPIView):
    """Adds a student to a class."""
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")

        student = get_object_or_404(UserProfile, id=self.request.data['student_id'])
        serializer.save(online_class=online_class, user_profile=student, role='student')



class RemoveStudentFromClass(DestroyAPIView):
    """Removes a student from a class."""
    permission_classes = [IsAuthenticated]
    queryset = ClassMembership.objects.all()

    def perform_destroy(self, instance):
        online_class = instance.online_class
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        instance.delete()


class EnterTheClassByPasswordView(CreateAPIView):
    """Handles class entry via password for private classes."""
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.is_private and online_class.entrance_code != self.request.data['entrance_code']:
            raise PermissionDenied("Invalid entrance code.")
        
        student = self.request.user.userprofile
        serializer.save(online_class=online_class, user_profile=student, role='student')


class SendInviteView(CreateAPIView):
    """Sends an invitation email to a user to join a private class."""
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")

        email = self.request.data['email']
        send_mail(
            'Invitation to join class',
            f'You are invited to join the class {online_class.title}. Use the code {online_class.entrance_code} to enter.',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Invitation sent successfully."}, status=status.HTTP_200_OK)


class ConfirmEnrollmentView(RetrieveAPIView):
    """Confirms the enrollment of a user into a class."""
    permission_classes = [IsAuthenticated]
    queryset = ClassMembership.objects.all()
    serializer_class = ClassMembershipSerializer

    def get(self, request, *args, **kwargs):
        online_class = get_object_or_404(OnlineClass, pk=request.data['class_id'])
        student = request.user.userprofile
        membership = ClassMembership.objects.filter(online_class=online_class, user_profile=student).first()

        if not membership:
            raise PermissionDenied("You are not enrolled in this class.")
        
        return Response({"message": "You are successfully enrolled in this class."})
