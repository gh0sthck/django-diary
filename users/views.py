from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import RegisterForm
from users.models import DiaryUser


class RegisterView(FormView):
    model = DiaryUser
    form_class = RegisterForm 
    success_url = reverse_lazy("all_notes") 
    template_name ="users_register.html"
