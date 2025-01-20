from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django_email_verification import send_email, send_password

from notes.utils import authenticate_required
from users.forms import RegisterForm
from users.models import DiaryUser
from users.utils import send_change_email, token_valid


class RegisterView(FormView):
    model = DiaryUser
    form_class = RegisterForm
    success_url = reverse_lazy("all_notes")
    template_name = "users_register.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        return redirect("all_notes")

    def form_valid(self, form: RegisterForm):
        user: DiaryUser = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user=user)
        return redirect("email_verify")


class ProfileSettingsView(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        return render(request, "users_settings.html")


class EmailVerify(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        send_email(request.user)
        return render(request, "email_verify.html")


class PasswordChange(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        send_password(request.user)
        return render(request, "password_email_sent.html")


class EmailChange(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        send_change_email(request.user)
        return render(request, "email_change_email_sent.html")


class EmailChanged(View):
    @authenticate_required
    def get(self, request: HttpRequest, token: str):
        return render(request, "email_change_template.html")

    @authenticate_required
    def post(self, request: HttpRequest, token: str):
        new_email = request.POST.get("email")
        success = False 
        if new_email:
            user: DiaryUser = DiaryUser.objects.get(id=request.user.id)
            if token_valid(token, user):  
                success = True
                user.email = new_email
                user.is_verified = False
                user.save() 
        return render(request, "email_changed_template.html", {"success": success})
