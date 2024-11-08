from django.db import models
from django.utils import timezone
from userapp.models import UserProfile

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    max_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    online_class = models.ForeignKey('class.OnlineClass', on_delete=models.CASCADE, related_name='exercises', default=1)

    def __str__(self):
        return f"{self.title} in {self.online_class.title}"


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='submissions', null=True)
    code = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    submission_date = models.DateTimeField(blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.user_profile} for {self.exercise.title}"


class Grading(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grading')
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    graded_by = models.ForeignKey(UserProfile, related_name='graded_submissions', on_delete=models.SET_NULL, null=True)
    feedback = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Grading for {self.submission} by {self.graded_by}"


class ExerciseMember(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    has_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_profile', 'exercise')

    def __str__(self):
        return f"{self.user_profile} for {self.exercise.title}"
