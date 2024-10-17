from django.urls import path
from .views import (
    CreateExercise,
    ListExercises,
    RetrieveExercise,
    CreateSubmission,
    RetrieveSubmission,
    CreateGrading,
)

urlpatterns = [
    path('exercises/', ListExercises.as_view(), name='list_exercises'),
    path('exercises/create/', CreateExercise.as_view(), name='create_exercise'),
    path('exercises/<int:pk>/', RetrieveExercise.as_view(), name='retrieve_exercise'),
    path('submissions/create/', CreateSubmission.as_view(), name='create_submission'),
    path('submissions/<int:pk>/', RetrieveSubmission.as_view(), name='retrieve_submission'),
    path('gradings/create/', CreateGrading.as_view(), name='create_grading'),
]
