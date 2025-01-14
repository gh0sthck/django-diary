from typing import Callable

from django.shortcuts import redirect


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
