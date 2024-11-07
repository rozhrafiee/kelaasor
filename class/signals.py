from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClassMembership, OnlineClass

@receiver(post_save, sender=ClassMembership)
def add_user_to_class(sender, instance, created, **kwargs):
    """Signal to automatically add user to the list of students upon class enrollment."""
    if created and instance.role == 'student':
        online_class = instance.online_class
        # Ensure the student is added to the class's students list
        online_class.students.add(instance.user_profile)
        online_class.save()
