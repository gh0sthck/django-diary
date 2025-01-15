from typing import Callable

from django.shortcuts import redirect
from django.urls import reverse
import markdown
from markdown.inlinepatterns import LinkInlineProcessor, LINK_RE

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


class SlugFieldLinkInlineProcessor(LinkInlineProcessor):
    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        if href.startswith("slug"):
            slug = href.split(":")[1]
            href = reverse("current_note", args=[slug])
        return href, title, index, handled
    

class SlugFieldExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SlugFieldLinkInlineProcessor(LINK_RE, md), "link", 160
        )
