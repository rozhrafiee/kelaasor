from django.db import models
from django.contrib.auth.models import User

# UserProfile model that extends the User model to include the user's role and additional information.
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('professor', 'Professor'),  # Role for professors
        ('student', 'Student'),  # Role for students
        ('mentor', 'Mentor'),  # Role for mentors
    ]
    
    # Linking the User model to the UserProfile with a one-to-one relationship.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # The role the user has (professor, student, or mentor)
    description = models.TextField(blank=True, null=True)  # Optional description for the user

    def __str__(self):
        return f"{self.user.username} - {self.role}"  # Represent the user profile with username and role
