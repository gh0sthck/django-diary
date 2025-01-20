from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import EmailChange, EmailChanged, EmailVerify, ProfileSettingsView, RegisterView, PasswordChange
from .forms import AuthForm

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users_login.html", authentication_form=AuthForm), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("settings/", ProfileSettingsView.as_view(), name="profile_settings"),
    path("email_verify/", EmailVerify.as_view(), name="email_verify"),
    path("change_pass/", PasswordChange.as_view(), name="change_passwd"),
    path("change_email/", EmailChange.as_view(), name="change_email"),
    path("change_email/<str:token>", EmailChanged.as_view(), name="changed_email")
    
]
