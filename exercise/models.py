from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.title
    
class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    code_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.exercise.title}"
    
class Grading(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    auto_score = models.IntegerField(null=True, blank=True)
    manual_score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def total_score(self):
        if self.manual_score is not None:
            return self.manual_score
        return self.auto_score    