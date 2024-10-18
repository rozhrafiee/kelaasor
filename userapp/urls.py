from django.urls import path
from .views import Login, Refresh, Register, UserProfileView, ChangePasswordView

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('refresh/', Refresh.as_view(), name='token_refresh'),
    path('register/', Register.as_view(), name='register'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('user/<str:username>/change-password/', ChangePasswordView.as_view(), name='change_password'),
]
