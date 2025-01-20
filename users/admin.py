from django.contrib import admin

from users.models import DiaryUser


@admin.register(DiaryUser)
class DiaryUserAdmin(admin.ModelAdmin):
    list_display = ["username"]
    search_fields = ["username"]
