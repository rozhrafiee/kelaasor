from django.db import models
from django.contrib.auth.models import User
from userapp.models import UserProfile  # Adjust as needed based on your project structure

class OnlineClass(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_classes')

    def __str__(self):
        return self.title

class ClassMembership(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor'),
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    online_class = models.ForeignKey(OnlineClass, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user_profile', 'online_class', 'role')
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.role} in {self.online_class.title}"
