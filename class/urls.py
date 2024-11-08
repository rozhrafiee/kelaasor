from django.urls import path
from .views import (
    CreateOnlineClass, UpdateOnlineClass, ListOnlineClasses, RetrieveOnlineClass,
    AddMentorToClass, AddTeacherToClass, AddStudentToClass, RemoveStudentFromClass,
     SendInviteView, ConfirmEnrollmentView,ListAllOnlineClasses, EnterTheClassByPasswordView
)

urlpatterns = [
    path('create/', CreateOnlineClass.as_view(), name='create_online_class'),
    path('update/<int:pk>/', UpdateOnlineClass.as_view(), name='update_online_class'),
    path('list/', ListAllOnlineClasses.as_view(), name='list_online_classes'),
    path('retrieve/<int:pk>/', RetrieveOnlineClass.as_view(), name='retrieve_online_class'),
    path('add-mentor/', AddMentorToClass.as_view(), name='add_mentor_to_class'),
    path('add-teacher/', AddTeacherToClass.as_view(), name='add_teacher_to_class'),
    path('add-student/', AddStudentToClass.as_view(), name='add_student_to_class'),
    path('remove-student/<int:pk>/', RemoveStudentFromClass.as_view(), name='remove_student_from_class'),
    path('enter/', EnterTheClassByPasswordView.as_view(), name='enter_class'),
    path('send-invite/', SendInviteView.as_view(), name='send_invite'),
    path('confirm-enrollment/', ConfirmEnrollmentView.as_view(), name='confirm_enrollment'),
]
