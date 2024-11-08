from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Exercise, Submission, Grading
from .serializers import ExerciseSerializer, SubmissionSerializer, GradingSerializer
from userapp.models import UserProfile


class CreateExercise(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer

    def perform_create(self, serializer):
        creator = self.request.user.userprofile
        serializer.save(created_by=creator)


class ListExercises(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_queryset(self):
        return Exercise.objects.filter(created_by=self.request.user.userprofile)


class RetrieveExercise(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


class SubmitAssignment(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        exercise = get_object_or_404(Exercise, pk=self.request.data['exercise_id'])
        student = self.request.user.userprofile
        serializer.save(exercise=exercise, student=student)


class ListSubmissions(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user.userprofile)


class GradeSubmission(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = GradingSerializer

    def perform_update(self, serializer):
        submission = self.get_object()
        if submission.exercise.created_by != self.request.user.userprofile:
            return Response(
                {"detail": "You are not the creator of this exercise."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class DeleteSubmission(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()

    def perform_destroy(self, instance):
        if instance.student != self.request.user.userprofile:
            return Response(
                {"detail": "You are not allowed to delete this submission."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class GradeReport(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Grading.objects.all()
    serializer_class = GradingSerializer

    def get(self, request, *args, **kwargs):
        submission = get_object_or_404(Submission, pk=self.kwargs['pk'])
        grading = get_object_or_404(Grading, submission=submission)
        return Response(GradingSerializer(grading).data)
