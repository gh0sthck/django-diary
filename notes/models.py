from django.db import models
from django.urls import reverse

from users.models import DiaryUser


class Note(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=80, null=False)
    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True) 
    text = models.TextField(verbose_name="Текст записи", null=True, blank=True)
    update_date = models.DateTimeField(verbose_name="Время обновления", auto_now=True)
    author = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, verbose_name="Автор")
  
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})
     
    def __str__(self):
        return self.title
   
    def __repr__(self) -> str:
        return f"<Note: {self.title}>"
    
    class Meta:
        ordering = ["-title", "create_date"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи" 
