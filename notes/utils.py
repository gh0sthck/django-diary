from typing import Callable, Optional

from django.shortcuts import redirect

from .models import Note


def authenticate_required(func: Callable):
    """
    I create new auth decorator, because django decorator `login_required`
    not normal work for my CBV views.
    """

    def wrapper(*args, **kwargs):
        if args[1].user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect("login")

    return wrapper


def email_verified_required(func: Callable):
    def wrapper(*args, **kwargs):
        if args[1].user.is_verified:
            return func(*args, **kwargs)
        return redirect("profile_settings")

    return wrapper


def get_note(slug: str, author_id: int) -> Optional[Note]:
    """Return note by slug and user id with orm optimezed query."""

    note = (
        Note.objects.filter(slug=slug, author=author_id)
        .select_related("author")
        .prefetch_related("tags")
    )
    return note[0] if note else None
