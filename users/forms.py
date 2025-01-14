from django import forms

from users.models import DiaryUser


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(
        max_length=128,
        min_length=8,
        label="Повтор пароля",
        widget=forms.PasswordInput,
    )

    def clean_password(self):
        data = self.cleaned_data
        if self.data["password_repeat"] == data["password"]:
            return data["password"]
        raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = DiaryUser
        fields = ["username", "email", "password"]
        widgets = {"password": forms.PasswordInput}
