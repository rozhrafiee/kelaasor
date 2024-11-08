from rest_framework import serializers
from .models import Exercise, Submission, Grading


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class GradingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grading
        fields = '__all__'
