from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView, CreateView

from notes.forms import NoteForm
from notes.models import Note


class AllUserNotes(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            user_id: int = request.user.id
            user_notes = Note.objects.filter(author=user_id).select_related("author") 
            return render(request, "notes_all.html", {"notes": user_notes}) 
        return redirect("auth")


class CurrentNote(View):
    def get(self, request: HttpRequest, slug: str):
        if request.user.is_authenticated:
            note = Note.objects.get(slug=slug)
            if note.author == request.user:
                return render(request, "notes_current.html", {"note": note})
            return redirect("all_notes")
        return redirect("auth")
    

class EditNote(UpdateView):
    model = Note
    form = NoteForm
    fields = ["title", "text"]
    template_name = "notes_edit.html"


class CreateNote(CreateView):
    model = Note
    fields = ["title", "text"] 
    template_name = "notes_edit.html"

    def post(self, request: HttpRequest):
        if request.user.is_authenticated: 
            form = NoteForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.author = request.user
                data.save() 
                return redirect("all_notes")
        return redirect("auth")


class DeleteNote(DeleteView):
    model = Note
    success_url = reverse_lazy("all_notes")
    template_name = "note_delete.html"
    context_object_name = "note"

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated: 
            author = self.get_object().author
            if request.user == author:
                return super().post(request, *args, **kwargs)
            return redirect("all_notes")
        return redirect("auth")
