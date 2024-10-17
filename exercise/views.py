from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Exercise, Submission, Grading
from .serializers import ExerciseSerializer, SubmissionSerializer, GradingSerializer
from django.core.exceptions import PermissionDenied

class CreateExercise(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        # Ensure that only instructors can create exercises
        if not self.request.user.is_staff:
            return Response({"message": "You do not have permission to create exercises."}, status=status.HTTP_403_FORBIDDEN)
        return super().perform_create(serializer)

class ListExercises(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.all()

class SubmitAssignment(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        # Associate the user with the submission
        serializer.save(student=self.request.user)

class ListSubmissions(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        exercise_id = self.request.query_params.get('exercise_id')
        if exercise_id:
            exercise = get_object_or_404(Exercise, id=exercise_id)
            return Submission.objects.filter(exercise=exercise, student=self.request.user)
        return Submission.objects.none()

class GradeSubmission(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GradingSerializer

    def get_object(self):
        submission_id = self.kwargs['submission_id']
        submission = get_object_or_404(Submission, id=submission_id)
        # Ensure that only instructors can grade submissions
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to grade submissions.")
        return submission

    def perform_update(self, serializer):
        serializer.save()
