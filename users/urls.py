from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import ProfileSettingsView, RegisterView
from .forms import AuthForm

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users_login.html", authentication_form=AuthForm), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("settings/", ProfileSettingsView.as_view(), name="profile_settings"),
]
