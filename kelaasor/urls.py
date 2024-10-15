from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from userapp.views import RegisterUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterUserView.as_view(), name='register'),  # Your registration URL
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain URL
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh URL
]