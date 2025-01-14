from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users_login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
