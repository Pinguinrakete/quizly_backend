from django.urls import path
from .views import RegisterView, CookieTokenObtainPairView, LogoutView, CookieTokenRefreshView

"""
    URL routes for authentication-related API endpoints.

    Includes endpoints for:
    - User registration
    - Login with JWT tokens (stored in cookies)
    - Logout and token invalidation
    - Refreshing access tokens using refresh cookies
"""
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CookieTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh')
]