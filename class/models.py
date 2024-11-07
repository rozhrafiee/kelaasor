from django.db import models
from django.conf import settings
from userapp.models import UserProfile  # Ensure this path matches your user model's actual location

class OnlineClass(models.Model):
    """Defines an online class with core details and access code."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)  
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_classes')

    def __str__(self):
        return f"{self.title} (Code: {self.code})"


class ClassMembership(models.Model):
    """Manages class membership and roles for users."""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor'),
    ]

    online_class = models.ForeignKey(OnlineClass, on_delete=models.CASCADE, related_name='memberships')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='class_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('online_class', 'user_profile')  # Ensures unique roles per user and class

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.role} in {self.online_class.title}"
