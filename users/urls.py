from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import (
    EmailChangeView,
    EmailChangedView,
    EmailVerifyView,
    ProfileSettingsView,
    RegisterView,
    PasswordChangeView,
)
from .forms import AuthForm

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="users_login.html", authentication_form=AuthForm
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("email_verify/", EmailVerifyView.as_view(), name="email_verify"),
    path("change_pass/", PasswordChangeView.as_view(), name="change_passwd"),
    path("change_email/", EmailChangeView.as_view(), name="change_email"),
    path("change_email/<str:token>", EmailChangedView.as_view(), name="changed_email"),
]
