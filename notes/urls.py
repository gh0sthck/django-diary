from django.urls import path

from notes.views import AllUserNotes, CreateNote, CurrentNote, DeleteNote, EditNote


urlpatterns = [
    path("", AllUserNotes.as_view(), name="all_notes"),
    path("create/", CreateNote.as_view(), name="create_note"),
    path("<slug:slug>/", CurrentNote.as_view(), name="current_note"),
    path("edit/<slug:slug>/", EditNote.as_view(), name="edit_note"),
    path("delete/<slug:slug>", DeleteNote.as_view(), name="delete_note"),
]
