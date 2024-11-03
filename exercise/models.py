from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'), 
        ('medium', 'Medium'), 
        ('hard', 'Hard')
    ])
    group_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    ANSWER_FORMAT_CHOICES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('code', 'Code'),
    ]
    answer_format = models.CharField(choices=ANSWER_FORMAT_CHOICES, max_length=10)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions')
    description = models.TextField()
    has_time_limit = models.BooleanField(default=False)
    has_upload_limit = models.BooleanField(default=False)
    first_deadline = models.DateTimeField(blank=True, null=True)
    second_deadline = models.DateTimeField(blank=True, null=True)
    penalty_hour = models.IntegerField(blank=True, null=True)
    penalty = models.IntegerField(blank=True, null=True)
    upload_limit = models.IntegerField(blank=True, null=True)
    in_bank = models.BooleanField(default=False)
    max_score = models.IntegerField(default=100)
    is_team = models.BooleanField(default=False)
    scoring_way = models.IntegerField(default=0)
    num_students_in_each_team = models.IntegerField(blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.exercise.title} - {self.description[:50]}"


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey("userapp.UserProfile", on_delete=models.CASCADE)
    code_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username}'s submission for {self.exercise.title}"


class Grading(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grading')
    grader = models.ForeignKey("userapp.UserProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    auto_score = models.IntegerField(null=True, blank=True)
    manual_score = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    @property
    def total_score(self):
        return self.manual_score if self.manual_score is not None else self.auto_score

    def __str__(self):
        return f"Grading for {self.submission}"
