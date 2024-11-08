from django.db import models
from userapp.models import UserProfile  

class OnlineClass(models.Model):
    """Represents an online class with core details, capacity, and access control."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    teachers = models.ManyToManyField(UserProfile, blank=True, related_name="teachers")
    mentors = models.ManyToManyField(UserProfile, blank=True, related_name="mentors")
    students = models.ManyToManyField(UserProfile, blank=True, related_name="students")

    capacity = models.PositiveIntegerField(default=10)
    has_capacity_limit = models.BooleanField(default=False)

    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_classes')
    password = models.CharField(max_length=255, blank=True, null=True)

    is_private = models.BooleanField(default=False)
    entrance_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.title} (Code: {self.code})"


class ClassMembership(models.Model):
    """Manages class membership and user roles (student, professor, or mentor)."""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('mentor', 'Mentor'),
    ]

    online_class = models.ForeignKey(OnlineClass, on_delete=models.CASCADE, related_name='memberships')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='class_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('online_class', 'user_profile')

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.role} in {self.online_class.title}"
