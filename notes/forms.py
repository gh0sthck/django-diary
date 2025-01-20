from django import forms
from mdeditor.fields import MDEditorWidget

from notes.models import Note, Tag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "text"]
        widgets = {
            "text": MDEditorWidget,
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"placeholder": "Название"})}
