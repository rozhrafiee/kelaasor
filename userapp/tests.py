from django.test import TestCase
from django.contrib.auth.models import User
from userapp.models import UserProfile

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Ensure the test user and profile are created or fetched correctly
        self.user, created = User.objects.get_or_create(username="testuser", email="test@example.com")
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)

        # Ensure role is set, even if profile already exists
        if not self.profile.role:
            self.profile.role = 'student'
            self.profile.save()

    def test_user_profile_creation(self):
        user = User.objects.get(username="testuser")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.role, "student")

    def test_duplicate_profile(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user, defaults={'role': 'mentor'})
        self.assertFalse(created)  # Check that the profile wasn't recreated

    def test_profile_update(self):
        profile = UserProfile.objects.get(user=self.user)
        profile.role = "professor"
        profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.role, "professor")
