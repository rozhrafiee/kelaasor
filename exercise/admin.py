from django.contrib import admin
from .models import Exercise, Submission, Grading, ExerciseMember

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'max_grade', 'online_class']
    search_fields = ['title', 'online_class__title']
    list_filter = ['start_date', 'online_class']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'user_profile', 'submitted_at', 'grade']
    search_fields = ['exercise__title', 'user_profile__user__username']
    list_filter = ['submitted_at', 'grade']

class GradingAdmin(admin.ModelAdmin):
    list_display = ['submission', 'grade', 'graded_by', 'graded_at']
    search_fields = ['submission__exercise__title', 'graded_by__user__username']
    list_filter = ['graded_at', 'grade']

class ExerciseMemberAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'exercise', 'has_submitted']
    search_fields = ['user_profile__user__username', 'exercise__title']
    list_filter = ['has_submitted']

# Register the models with the admin site
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grading, GradingAdmin)
admin.site.register(ExerciseMember, ExerciseMemberAdmin)
