from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
import markdown
from pytils.translit import slugify
from mdeditor.fields import MDTextField

from users.models import DiaryUser


class Note(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=80, null=False)
    slug = models.SlugField(verbose_name="Слаг", max_length=128, unique=True)
    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True) 
    # text = models.TextField(verbose_name="Текст записи", null=True, blank=True)
    text = MDTextField(verbose_name="Текст записи", null=True, blank=True) 
    update_date = models.DateTimeField(verbose_name="Время обновления", auto_now=True)
    author = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, verbose_name="Автор")
  
    def get_absolute_url(self):
        return reverse("current_note", kwargs={"slug": self.slug})
   
    def text_as_markdown(self):
        return mark_safe(markdown.markdown(self.text))
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs) 
     
    def __str__(self):
        return self.title
   
    def __repr__(self) -> str:
        return f"<Note: {self.title}>"
    
    class Meta:
        ordering = ["-title", "create_date"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи" 
