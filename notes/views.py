from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic.edit import UpdateView, CreateView

from notes.forms import NoteForm
from notes.models import Note
from notes.utils import authenticate_required


class AllUserNotes(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        user_id: int = request.user.id
        match request.GET.get("notes_sort"):
            case "new":
                user_notes = Note.objects.order_by("-create_date").filter(
                    author=user_id
                )
            case "old":
                user_notes = Note.objects.order_by("create_date").filter(author=user_id)
            case "modify":
                user_notes = Note.objects.order_by("-update_date").filter(
                    author=user_id
                )
            case "az":
                user_notes = Note.objects.order_by("title").filter(author=user_id)
            case _:
                user_notes = Note.objects.filter(author=user_id)

        user_notes = user_notes.select_related("author")

        paginator = Paginator(user_notes, 4)
        page_number = request.GET.get("page")
        notes_per_page = paginator.get_page(page_number)
        pages = paginator.num_pages

        url = "?notes_sort="+request.GET.get("notes_sort") if request.GET.get("notes_sort") else ""
        url += "&page=" if url else "?page="

    
        return render(
            request, "notes_all.html", {"notes" : notes_per_page, "pages": pages, "url": url }
        )


class CurrentNote(View):
    @authenticate_required
    def get(self, request: HttpRequest, slug: str):
        note = Note.objects.get(slug=slug)
        if note.author == request.user:
            return render(request, "notes_current.html", {"note": note})
        return redirect("all_notes")


class EditNote(UpdateView):
    model = Note
    form = NoteForm
    fields = ["title", "text"]
    template_name = "notes_edit.html"

    @authenticate_required
    def get(self, request: HttpRequest, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateNote(CreateView):
    model = Note
    fields = ["title", "text"]
    template_name = "notes_edit.html"

    @authenticate_required
    def get(self, request: HttpRequest, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @authenticate_required
    def post(self, request: HttpRequest):
        form = NoteForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.save()
            return redirect("all_notes")


class DeleteNote(DeleteView):
    model = Note
    success_url = reverse_lazy("all_notes")
    template_name = "note_delete.html"
    context_object_name = "note"

    @authenticate_required
    def post(self, request: HttpRequest, *args, **kwargs):
        author = self.get_object().author
        if request.user == author:
            return super().post(request, *args, **kwargs)
        return redirect("all_notes")
