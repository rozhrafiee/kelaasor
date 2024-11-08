from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .models import OnlineClass, ClassMembership
from userapp.models import UserProfile
from .serializers import OnlineClassSerializer, ClassMembershipSerializer, EnterTheClassByPasswordSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class CreateOnlineClass(CreateAPIView):
    serializer_class = OnlineClassSerializer

    def create(self, request, *args, **kwargs):
        professor_username = request.data.get('professor_username')
        try:
            professor = User.objects.get(username=professor_username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Professor not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_class = OnlineClass.objects.create(
            title=request.data['title'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            created_by=professor.userprofile,
        )

        return Response(
            {"message": "Class created successfully", "class": OnlineClassSerializer(new_class).data},
            status=status.HTTP_201_CREATED
        )


class UpdateOnlineClass(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OnlineClass.objects.all()
    serializer_class = OnlineClassSerializer

    def perform_update(self, serializer):
        online_class = self.get_object()
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        serializer.save()


class ListOnlineClasses(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer

    def get_queryset(self):
        return OnlineClass.objects.filter(students=self.request.user.userprofile)


class RetrieveOnlineClass(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = OnlineClass.objects.all()
    serializer_class = OnlineClassSerializer


class AddMentorToClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        
        mentor = get_object_or_404(UserProfile, id=self.request.data['mentor_id'])
        serializer.save(online_class=online_class, user_profile=mentor, role='mentor')


class AddTeacherToClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        
        teacher = get_object_or_404(UserProfile, id=self.request.data['teacher_id'])
        serializer.save(online_class=online_class, user_profile=teacher, role='professor')


class AddStudentToClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassMembershipSerializer

    def perform_create(self, serializer):
        online_class = get_object_or_404(OnlineClass, pk=self.request.data['class_id'])
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")

        student = get_object_or_404(UserProfile, id=self.request.data['student_id'])
        serializer.save(online_class=online_class, user_profile=student, role='student')


class RemoveStudentFromClass(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ClassMembership.objects.all()

    def perform_destroy(self, instance):
        online_class = instance.online_class
        if online_class.created_by != self.request.user.userprofile:
            raise PermissionDenied("You are not the professor of this class.")
        instance.delete()


class EnterTheClassByPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = EnterTheClassByPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            userprofile = request.user.userprofile
            online_class_code = serializer.validated_data['code']
            password = serializer.validated_data['password']

            # Get the OnlineClass object using the class code
            online_class = OnlineClass.objects.get(code=online_class_code)

            # Check if the user is already a member of the class
            if userprofile in online_class.students.all() or userprofile in online_class.mentors.all() or userprofile in online_class.teachers.all():
                return Response({'message': 'You are already a member of this class'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the provided password matches the hashed password in the database
            if not check_password(password, online_class.password):  # Correct way to check against hashed password
                return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

            # Add the user to the class's student list
            online_class.students.add(userprofile)
            
            return Response({'message': 'Password is correct and you are added to the class'}, status=status.HTTP_200_OK)
        
        except OnlineClass.DoesNotExist:    
            return Response({'message': 'Online class not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Catch any other exceptions and return an appropriate error message
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendInviteView(CreateAPIView):
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


class ListAllOnlineClasses(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnlineClassSerializer

    def get_queryset(self):
        return OnlineClass.objects.all()
