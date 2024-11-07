from django.urls import path
from userapp import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Endpoint for registering a new user. This will handle POST requests to create a user with a role.
    path('register/', views.UserRegisterView.as_view(), name='user-register'),

    # Endpoint for updating the user's profile. Only allows updating description.
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),

    # Endpoint for logging in and obtaining the JWT tokens.
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access and refresh tokens
    
    # Endpoint for refreshing the JWT tokens when the access token expires.
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the JWT token
]
