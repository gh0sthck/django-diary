from django import forms
from mdeditor.fields import MDEditorWidget

from notes.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "text"]
        widgets = {"text": MDEditorWidget}
