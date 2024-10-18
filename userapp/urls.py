from django.urls import path
from .views import Register, Login, ChangePassword

urlpatterns = [
    path('register/', Register.as_view(), name='register'),  # Endpoint for user registration
    path('login/', Login.as_view(), name='login'),           # Endpoint for user login
    path('change-password/', ChangePassword.as_view(), name='change-password'),  # Endpoint for changing password
]
