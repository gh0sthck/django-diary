from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView

from notes.forms import CreateTagForm, NoteForm
from notes.models import Note, Tag
from notes.utils import authenticate_required


class AllUserNotes(View):
    @authenticate_required
    def get(self, request: HttpRequest):
        user_id: int = request.user.id
        user_notes = Note.objects 
        url = ""
        
        if request.GET.get("notes_sort_tag"):
            tag_sort = request.GET.get("notes_sort_tag")
            user_notes = user_notes.filter(tags__name=tag_sort)
            url = "?notes_sort_tag=" + tag_sort
        
        match request.GET.get("notes_sort"):
            case "new":
                user_notes = user_notes.order_by("-create_date").filter(
                    author=user_id
                )
            case "old":
                user_notes = user_notes.order_by("create_date").filter(author=user_id)
            case "modify":
                user_notes = user_notes.order_by("-update_date").filter(
                    author=user_id
                )
            case "az":
                user_notes = user_notes.order_by("title").filter(author=user_id)
            case _:
                user_notes = user_notes.filter(author=user_id)

        user_notes = user_notes.select_related("author")

        tags = Tag.objects.filter(note__author=request.user).distinct()

        paginator = Paginator(user_notes, 4)
        page_number = request.GET.get("page")
        notes_per_page = paginator.get_page(page_number)
        pages = paginator.num_pages

        if request.GET.get("notes_sort"):
            if url:
                url += "&notes_sort=" + request.GET.get("notes_sort")
            else:
                url = "?notes_sort=" + request.GET.get("notes_sort")
        
        url += "&page=" if url else "?page="

        return render(
            request,
            "notes_all.html",
            {"notes": notes_per_page, "pages": pages, "url": url, "tags": tags},
        )


class CurrentNote(View):
    @authenticate_required
    def get(self, request: HttpRequest, slug: str):
        note = Note.objects.filter(slug=slug, author=request.user.id)
        if note:
            note = note[0]
            tags = (
                Tag.objects.filter(note__author=request.user)
                .exclude(note__id=note.id)
                .distinct()
            )
            return render(
                request,
                "notes_current.html",
                {"note": note, "create_tag_form": CreateTagForm(), "all_tags": tags},
            )
        return redirect("all_notes")


class EditNote(View):
    @authenticate_required
    def get(self, request: HttpRequest, slug: str):
        note = Note.objects.filter(slug=slug, author=request.user.id)
        if note:
            return render(
                request, "notes_edit.html", {"form": NoteForm(note[0].__dict__)}
            )

    @authenticate_required
    def post(self, request: HttpRequest, slug: str):
        form = NoteForm(request.POST)
        if form.is_valid():
            if note := Note.objects.filter(author=request.user.id, slug=slug):
                note: Note = note[0]

                note.title = form.cleaned_data["title"]
                note.text = form.cleaned_data["text"]
                note.save()
                return redirect("current_note", note.slug)


class CreateNote(CreateView):
    model = Note
    template_name = "notes_edit.html"
    form_class = NoteForm

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


class DeleteNote(View):
    @authenticate_required
    def get(self, request: HttpRequest, slug: str):
        note = Note.objects.filter(author=request.user.id, slug=slug)
        if note:
            note = note[0]
            return render(request, "notes_delete.html", {"note": note})
        return redirect("all_notes")

    @authenticate_required
    def post(self, request: HttpRequest, slug: str):
        note = Note.objects.filter(slug=slug, author=request.user.id)
        note.delete()
        return redirect("all_notes")


class CreateTag(View):
    @authenticate_required
    def post(self, request: HttpRequest):
        form = CreateTagForm(request.POST)
        note = Note.objects.get(id=request.POST.get("note_id"))
        if form.is_valid():
            tag: Tag = form.save(commit=False)
            tags = Tag.objects.filter(note__author=request.user.id)
            if tag.name not in list(tag.name for tag in tags):
                tag.save()
            else:
                tag = Tag.objects.filter(note__author=request.user.id, name=tag.name)[0]
            if tag.name not in list(tag.name for tag in note.tags.iterator()):
                note.tags.add(tag)
            return redirect("current_note", note.slug)
        return redirect("current_note", note.slug)


class DeleteTag(View):
    @authenticate_required
    def post(self, request: HttpRequest):
        id_ = request.POST.get("tag_pk")
        note_id = request.POST.get("note_pk")

        note = Note.objects.get(id=note_id)
        tag = Tag.objects.get(id=id_)
        if Note.objects.filter(tags__id=id_).count() == 1:
            tag.delete()
            note.tags.remove(tag)
        else:
            note.tags.remove(tag)

        return redirect("current_note", note.slug)
