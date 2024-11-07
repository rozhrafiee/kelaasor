from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import OnlineClass, UserProfile, ClassMembership
from .serializers import AddUserToClassSerializer, OnlineClassSerializer
from django.contrib.auth.models import User


# Create a new class

class CreateClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OnlineClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        online_class = serializer.save(created_by=request.user.userprofile)
        return Response({'message': 'Class created successfully', 'class': serializer.data}, status=status.HTTP_201_CREATED)

# Update an existing class

class UpdateClassView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        online_class = get_object_or_404(OnlineClass, id=pk)
        serializer = OnlineClassSerializer(online_class, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        return Response({'message': 'Class updated successfully', 'class': serializer.data}, status=status.HTTP_200_OK)

# Show mentors, teachers, and students of a class

class ShowClassMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        online_class = get_object_or_404(OnlineClass, id=pk)
        mentors = online_class.mentors.all().values('id', 'user__username')
        teachers = online_class.teachers.all().values('id', 'user__username')
        students = online_class.students.all().values('id', 'user__username')

        return Response({
            'mentors': list(mentors),
            'teachers': list(teachers),
            'students': list(students)
        }, status=status.HTTP_200_OK)

# Enter a class by code and password

class EnterClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_code = request.data.get("code")
        password = request.data.get("password")
        
        try:
            online_class = OnlineClass.objects.get(code=class_code)
            if online_class.password != password:
                return Response({'error': 'Invalid password'}, status=status.HTTP_403_FORBIDDEN)
            return Response({'message': 'Successfully entered the class', 'class_id': online_class.id}, status=status.HTTP_200_OK)
        except OnlineClass.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

# Add and remove a teacher

class AddTeacherView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        teacher_username = serializer.validated_data['username']
        
        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            teacher = User.objects.get(username=teacher_username).userprofile
            online_class.teachers.add(teacher)
            return Response({'message': 'Teacher successfully added.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)

class RemoveTeacherView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        teacher_username = serializer.validated_data['username']

        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            teacher = User.objects.get(username=teacher_username).userprofile
            online_class.teachers.remove(teacher)
            return Response({'message': 'Teacher successfully removed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found.'}, status=status.HTTP_404_NOT_FOUND)

# Add and remove a mentor

class AddMentorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        mentor_username = serializer.validated_data['username']

        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            mentor = User.objects.get(username=mentor_username).userprofile
            online_class.mentors.add(mentor)
            return Response({'message': 'Mentor successfully added.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Mentor not found.'}, status=status.HTTP_404_NOT_FOUND)

class RemoveMentorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        mentor_username = serializer.validated_data['username']

        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            mentor = User.objects.get(username=mentor_username).userprofile
            online_class.mentors.remove(mentor)
            return Response({'message': 'Mentor successfully removed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Mentor not found.'}, status=status.HTTP_404_NOT_FOUND)

# Add and remove a student

class AddStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        student_username = serializer.validated_data['username']

        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            student = User.objects.get(username=student_username).userprofile
            online_class.students.add(student)
            return Response({'message': 'Student successfully added.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

class RemoveStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserToClassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        class_code = serializer.validated_data['code']
        student_username = serializer.validated_data['username']

        online_class = get_object_or_404(OnlineClass, code=class_code)
        try:
            student = User.objects.get(username=student_username).userprofile
            online_class.students.remove(student)
            return Response({'message': 'Student successfully removed.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
