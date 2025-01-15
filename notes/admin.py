from django.contrib import admin

from notes.models import Note, Tag


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title", "create_date", "update_date"]
    prepopulated_fields = {"slug": ("title", )}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    