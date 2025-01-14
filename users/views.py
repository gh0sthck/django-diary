from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from notes.utils import authenticate_required
from users.forms import RegisterForm
from users.models import DiaryUser


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
        return redirect("all_notes") 


class ProfileSettingsView(View):
    def get(self, request: HttpRequest):
        return render(request, "users_settings.html")
