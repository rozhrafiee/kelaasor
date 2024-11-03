from django.urls import path
from . import views

urlpatterns = [
    path('classes/create/', views.CreateOnlineClassView.as_view(), name='create_online_class'),
    path('classes/', views.ListOnlineClassesView.as_view(), name='list_online_classes'),
    path('classes/<int:id>/', views.RetrieveOnlineClassView.as_view(), name='retrieve_online_class'),
    path('memberships/create/', views.CreateClassMembershipView.as_view(), name='create_class_membership'),
]
