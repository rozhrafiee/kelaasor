from django.urls import path
from .views import (
    CreateOnlineClass, UpdateOnlineClass, ListOnlineClasses, RetrieveOnlineClass,
    AddMentorToClass, AddTeacherToClass, RemoveStudentFromClass, EnterTheClassByPasswordView,
    SendInviteView, ConfirmEnrollmentView, AddStudentToClass
)

urlpatterns = [
    path('classes/create/', CreateOnlineClass.as_view(), name='create_class'),
    path('classes/update/<int:pk>/', UpdateOnlineClass.as_view(), name='update_class'),
    path('classes/', ListOnlineClasses.as_view(), name='list_classes'),
    path('classes/<int:pk>/', RetrieveOnlineClass.as_view(), name='retrieve_class'),
    path('classes/add-mentor/', AddMentorToClass.as_view(), name='add_mentor_to_class'),
    path('classes/add-teacher/', AddTeacherToClass.as_view(), name='add_teacher_to_class'),
    path('classes/remove-student/', RemoveStudentFromClass.as_view(), name='remove_student_from_class'),
    path('classes/add-student/', AddStudentToClass.as_view(), name='add_student_to_class'),
    path('classes/enter-by-password/', EnterTheClassByPasswordView.as_view(), name='enter_class_by_password'),
    path('classes/send-invite/', SendInviteView.as_view(), name='send_invite_to_class'),
    path('classes/confirm-enrollment/', ConfirmEnrollmentView.as_view(), name='confirm_enrollment')
]
