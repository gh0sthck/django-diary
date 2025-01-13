from django.urls import path

from notes.views import AllUserNotes


urlpatterns = [
    path("all/", AllUserNotes.as_view(), name="all"),
]
