from django.urls import path
from .views import (
    CreateOnlineClass, UpdateOnlineClass, AddMentorToClass, OnlineClassViewStudentsView,
    AddTeacherToClass, RemoveStudentFromClass, EnterTheClassByPasswordView,
    SendInviteView, ConfirmEnrollmentView, StudentClassView, StudentAddView
)

urlpatterns = [
    path('class/create-new/', CreateOnlineClass.as_view(), name='class-create-new'),
    path('class/edit/<int:pk>/', UpdateOnlineClass.as_view(), name='class-edit'),
    path('class/assign-mentor/', AddMentorToClass.as_view(), name='class-assign-mentor'),
    path('class/students/list/<int:pk>/', OnlineClassViewStudentsView.as_view(), name='class-student-list'),
    path('class/assign-teacher/', AddTeacherToClass.as_view(), name='class-assign-teacher'),
    path('class/student/remove/', RemoveStudentFromClass.as_view(), name='class-student-remove'),
    path('class/access/', EnterTheClassByPasswordView.as_view(), name='class-access-by-password'),
    path('class/invite/send/', SendInviteView.as_view(), name='class-invite-send'),
    path('class/enrollment/confirm/', ConfirmEnrollmentView.as_view(), name='class-enrollment-confirm'),
    path('class/student/view/', StudentClassView.as_view(), name='class-student-view'),
    path('class/student/add/', StudentAddView.as_view(), name='class-student-add'),
]
