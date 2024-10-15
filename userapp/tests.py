from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, role='student')

    def test_user_profile_creation(self):
        self.assertEqual(self.user.userprofile.role, 'student')
