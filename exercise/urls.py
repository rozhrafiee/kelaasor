from django.urls import path
from .views import (
    CreateExercise, ListExercises, RetrieveExercise, SubmitAssignment, ListSubmissions,
    GradeSubmission, DeleteSubmission, GradeReport
)

urlpatterns = [
    path('create/', CreateExercise.as_view(), name='create_exercise'),
    path('list/', ListExercises.as_view(), name='list_exercises'),
    path('retrieve/<int:pk>/', RetrieveExercise.as_view(), name='retrieve_exercise'),
    path('submit/', SubmitAssignment.as_view(), name='submit_assignment'),
    path('submissions/', ListSubmissions.as_view(), name='list_submissions'),
    path('grade/<int:pk>/', GradeSubmission.as_view(), name='grade_submission'),
    path('delete-submission/<int:pk>/', DeleteSubmission.as_view(), name='delete_submission'),
    path('grade-report/<int:pk>/', GradeReport.as_view(), name='grade_report'),
]
