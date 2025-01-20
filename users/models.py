from django.db import models
from django.contrib.auth.models import AbstractUser

class DiaryUser(AbstractUser):
    username = models.CharField(verbose_name="Имя пользователя", unique=True, null=False, max_length=80)
    email = models.EmailField(verbose_name="Электронная почта", unique=True, null=False)
    is_verified = models.BooleanField(verbose_name="Подтверждение почты", default=False)

    def __repr__(self) -> str:
        return f"<DiaryUser: {self.username}>"

    def __str__(self) -> str:
        return self.username

    class Meta:
        ordering = ["-username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
