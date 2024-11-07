from django.urls import path
from .views import (
    CreateClassView,
    UpdateClassView,
    ShowClassMembersView,
    EnterClassView,
    AddTeacherView,
    RemoveTeacherView,
    AddMentorView,
    RemoveMentorView,
    AddStudentView,
    RemoveStudentView,
)

urlpatterns = [
    path('class/create/', CreateClassView.as_view(), name='create_class'),
    path('class/update/<int:pk>/', UpdateClassView.as_view(), name='update_class'),
    path('class/<int:pk>/members/', ShowClassMembersView.as_view(), name='show_class_members'),
    path('class/enter/', EnterClassView.as_view(), name='enter_class'),
    
    path('class/add-teacher/', AddTeacherView.as_view(), name='add_teacher'),
    path('class/remove-teacher/', RemoveTeacherView.as_view(), name='remove_teacher'),
    
    path('class/add-mentor/', AddMentorView.as_view(), name='add_mentor'),
    path('class/remove-mentor/', RemoveMentorView.as_view(), name='remove_mentor'),
    
    path('class/add-student/', AddStudentView.as_view(), name='add_student'),
    path('class/remove-student/', RemoveStudentView.as_view(), name='remove_student'),
]
