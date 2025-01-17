from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

from users.models import DiaryUser


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(
        max_length=128,
        min_length=8,
        label="Повтор пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_password(self):
        data = self.cleaned_data
        if self.data["password_repeat"] == data["password"]:
            return data["password"]
        raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = DiaryUser
        fields = ["username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class AuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )
