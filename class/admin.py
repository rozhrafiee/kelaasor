from django.contrib import admin
from .models import OnlineClass, ClassMembership

# Registering the OnlineClass model to the admin panel
class OnlineClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'created_by', 'is_private')  # Fields you want to display
    search_fields = ('title', 'created_by__user__username')  # Make title and professor username searchable
    list_filter = ('is_private',)  # You can filter by class type

admin.site.register(OnlineClass, OnlineClassAdmin)

# Register ClassMembership if you want to manage memberships in the admin panel
class ClassMembershipAdmin(admin.ModelAdmin):
    list_display = ('online_class', 'user_profile', 'role')  # Display the class, user and their role
    search_fields = ('online_class__title', 'user_profile__user__username')  # Make online class title and user username searchable

admin.site.register(ClassMembership, ClassMembershipAdmin)
