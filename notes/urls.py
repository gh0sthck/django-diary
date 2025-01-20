from django.urls import path

from notes.views import (
    AllUserNotesView,
    CreateNoteView,
    CreateTagView,
    CurrentNoteView,
    DeleteNoteView,
    DeleteTagView,
    EditNoteView,
)


urlpatterns = [
    path("", AllUserNotesView.as_view(), name="all_notes"),
    path("create_tag/", CreateTagView.as_view(), name="create_tag"),
    path("delete_tag/", DeleteTagView.as_view(), name="delete_tag"),
    path("create/", CreateNoteView.as_view(), name="create_note"),
    path("<slug:slug>/", CurrentNoteView.as_view(), name="current_note"),
    path("edit/<slug:slug>/", EditNoteView.as_view(), name="edit_note"),
    path("delete/<slug:slug>", DeleteNoteView.as_view(), name="delete_note"),
]
