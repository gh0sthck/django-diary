from django import forms

from users.models import DiaryUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = DiaryUser
        fields = ["username", "password"]
