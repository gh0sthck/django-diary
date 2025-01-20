from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView

from notes.forms import CreateTagForm, NoteForm
from notes.models import Note, Tag
from notes.utils import authenticate_required, email_verified_required, get_note


class AllUserNotesView(View):
    """
    Main page.
    """

    @authenticate_required
    def get(self, request: HttpRequest):
        user_id: int = request.user.id
        user_notes = Note.objects
        url = ""

        # Add sort tags in url it indicate
        if request.GET.get("notes_sort_tag"):
            tag_sort = request.GET.get("notes_sort_tag")
            user_notes = user_notes.filter(tags__name=tag_sort)
            url = "?notes_sort_tag=" + tag_sort

        match request.GET.get("notes_sort"):
            case "new":
                user_notes = user_notes.order_by("-create_date").filter(author=user_id)
            case "old":
                user_notes = user_notes.order_by("create_date").filter(author=user_id)
            case "modify":
                user_notes = user_notes.order_by("-update_date").filter(author=user_id)
            case "az":
                user_notes = user_notes.order_by("title").filter(author=user_id)
            case _:
                user_notes = user_notes.filter(author=user_id)

        user_notes = user_notes.select_related("author").prefetch_related("tags")

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

        # Mandatory, regargdless of tags or notes sort
        url += "&page=" if url else "?page="

        return render(
            request,
            "notes_all.html",
            {"notes": notes_per_page, "pages": pages, "url": url, "tags": tags},
        )


class CurrentNoteView(View):
    @authenticate_required
    def get(self, request: HttpRequest, slug: str):
        if note := get_note(slug=slug, author_id=request.user.id):
            # Get tags, excluding tags which pinned to note
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


class EditNoteView(View):
    @authenticate_required
    @email_verified_required
    def get(self, request: HttpRequest, slug: str):
        if note := get_note(slug=slug, author_id=request.user.id):
            return render(request, "notes_edit.html", {"form": NoteForm(note.__dict__)})

    @authenticate_required
    @email_verified_required
    def post(self, request: HttpRequest, slug: str):
        form = NoteForm(request.POST)
        if form.is_valid():
            if note := get_note(slug=slug, author_id=request.user.id):
                note.title = form.cleaned_data["title"]
                note.text = form.cleaned_data["text"]
                note.save()
                return redirect("current_note", note.slug)


class CreateNoteView(CreateView):
    model = Note
    template_name = "notes_edit.html"
    form_class = NoteForm

    @authenticate_required
    @email_verified_required
    def get(self, request: HttpRequest, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @authenticate_required
    @email_verified_required
    def post(self, request: HttpRequest):
        form = NoteForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = request.user
            data.save()
            return redirect("all_notes")


class DeleteNoteView(View):
    @authenticate_required
    @email_verified_required
    def get(self, request: HttpRequest, slug: str):
        if note := get_note(slug=slug, author_id=request.user.id):
            return render(request, "notes_delete.html", {"note": note})
        return redirect("all_notes")

    @authenticate_required
    @email_verified_required
    def post(self, request: HttpRequest, slug: str):
        if note := get_note(slug=slug, author_id=request.user.id):
            note.delete()
        return redirect("all_notes")


class CreateTagView(View):
    """
    Create tag can executing only by post from specific CurrentNote.
    """

    @authenticate_required
    def post(self, request: HttpRequest):
        form = CreateTagForm(request.POST)
        # Get note by receiving data from specific note in hidden field
        note = Note.objects.get(id=request.POST.get("note_id"))
        if form.is_valid():
            tag: Tag = form.save(commit=False)
            # Getting all tags by current user
            tags = Tag.objects.filter(note__author=request.user.id)
            if tag.name not in list(tag.name for tag in tags):
                tag.save()  # Save tag only if it not created by user
            else:
                # Else get already exist tag
                tag = Tag.objects.filter(note__author=request.user.id, name=tag.name)[0]
            if tag.name not in list(tag.name for tag in note.tags.iterator()):
                note.tags.add(tag)  # Tag add to note only if it not added
            return redirect("current_note", note.slug)
        return redirect("current_note", note.slug)


class DeleteTagView(View):
    """
    Delete tag can executing only by post from specific CurrentNote.
    """

    @authenticate_required
    def post(self, request: HttpRequest):
        id_ = request.POST.get("tag_pk")
        note_id = request.POST.get("note_pk")

        note = Note.objects.get(id=note_id)
        tag = Tag.objects.get(id=id_)

        # If specific note have only one specific tag - tag will delete: from note and database
        if Note.objects.filter(tags__id=id_).count() == 1:
            tag.delete()
            note.tags.remove(tag)
        # If tag exists in other note - tag will delet only from specific note
        else:
            note.tags.remove(tag)

        return redirect("current_note", note.slug)
