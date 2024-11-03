from django.urls import path
from .views import (
    CreateExercise,
    ListExercises,
    CreateSubmission,
    ListSubmissions,
    CreateGrading,
    ExerciseEditView,
    
)

urlpatterns = [
    path('exercises/', ListExercises.as_view(), name='list_exercises'),  # List all exercises
    path('exercises/create/', CreateExercise.as_view(), name='create_exercise'),  # Create a new exercise
    path('submissions/', ListSubmissions.as_view(), name='list_submissions'),  # List submissions for an exercise
    path('submissions/create/', CreateSubmission.as_view(), name='create_submission'),  # Create a new submission
    path('grading/create/', CreateGrading.as_view(), name='create_grading'),  # Create a new grading entr
    path('exercises/<int:id>/edit/', ExerciseEditView.as_view(), name='edit-exercise'),
    # other URLs...
]

