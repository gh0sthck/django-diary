from ast import Not
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from notes.models import Note
from users.models import DiaryUser


class AllUserNotes(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            user: DiaryUser = request.user.id
            user_notes = Note.objects.filter(author=user).select_related("author") 
            return render(request, "notes.html", {"notes": user_notes}) 
        return redirect("auth")
