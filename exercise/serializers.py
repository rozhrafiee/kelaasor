from rest_framework import serializers
from .models import Exercise, Submission, Grading

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'description', 'due_date', 'max_score']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'exercise', 'user', 'code_file', 'submitted_at']

class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ['id', 'submission', 'auto_score', 'manual_score', 'feedback']

class CreateExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['title', 'description', 'due_date', 'max_score']

class CreateSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['exercise', 'code_file']

class CreateGradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = ['submission', 'auto_score', 'manual_score', 'feedback']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'description', 'due_date', 'max_score']