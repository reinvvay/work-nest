from django.urls import path

from accounts.views import (
    LoginView,
    SignupView,
    SignupSuccessView,
    LogoutView,
    ProfileUpdateView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("signup-success/", SignupSuccessView.as_view(), name="signup_success"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileUpdateView.as_view(), name="profile_update"),
]

app_name = "accounts"
