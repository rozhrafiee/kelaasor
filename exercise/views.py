from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ExerciseSerializer,
    CreateSubmissionSerializer,
    GradingSerializer,
)
from .models import Exercise, Submission, Grading
from rest_framework.permissions import IsAuthenticated

class CreateExercise(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()

    def perform_create(self, serializer):
        # Additional checks for creating exercises can be added here
        return super().perform_create(serializer)


class ListExercises(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        # You can filter exercises based on certain criteria
        return Exercise.objects.all()


class CreateSubmission(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSubmissionSerializer
    queryset = Submission.objects.all()

    def perform_create(self, serializer):
        student = self.request.user.userprofile
        exercise = serializer.validated_data['exercise']

        # Check if the student is allowed to submit for the exercise
        if student not in exercise.online_class.students.all():
            return Response({"message": "you can't submit for this exercise"}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(student=student)


class ListSubmissions(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSubmissionSerializer

    def get_queryset(self):
        exercise_id = self.request.query_params.get('exercise_id')
        if exercise_id:
            return Submission.objects.filter(exercise_id=exercise_id)
        return Submission.objects.none()


class CreateGrading(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GradingSerializer
    queryset = Grading.objects.all()

    def perform_create(self, serializer):
        submission = serializer.validated_data['submission']
        user_profile = self.request.user.userprofile
        
        # Check if the user is authorized to grade submissions
        if user_profile not in submission.exercise.online_class.teachers.all():
            return Response({"message": "you can't grade this submission"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()


class ExerciseEditView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
    lookup_field = 'id'  # Look up exercises by their ID in the URL

    def put(self, request, *args, **kwargs):
        exercise = self.get_object()
        user_profile = request.user.userprofile  # Assumes UserProfile has the role information

        # Check if the user is a teacher or mentor for permission to edit
        if user_profile not in exercise.online_class.teachers.all() and user_profile not in exercise.online_class.mentors.all():
            return Response({"message": "You don't have permission to edit this exercise."}, status=status.HTTP_403_FORBIDDEN)
        
        return self.update(request, *args, **kwargs)
