from django.urls import path

from notes.views import AllUserNotes, CreateNote, CreateTag, CurrentNote, DeleteNote, DeleteTag, EditNote


urlpatterns = [
    path("", AllUserNotes.as_view(), name="all_notes"),
    path("create_tag/", CreateTag.as_view(), name="create_tag"), 
    path("delete_tag/", DeleteTag.as_view(), name="delete_tag"),
    path("create/", CreateNote.as_view(), name="create_note"),
    path("<slug:slug>/", CurrentNote.as_view(), name="current_note"),
    path("edit/<slug:slug>/", EditNote.as_view(), name="edit_note"),
    path("delete/<slug:slug>", DeleteNote.as_view(), name="delete_note"), 
]
