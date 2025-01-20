import datetime
import time
from typing import Optional
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
import jwt


def encode_token(user) -> str:
    token = jwt.encode(
        payload={
            "email": user.email,
            "exp": datetime.datetime.now()
            + datetime.timedelta(seconds=settings.TOKEN_LIFE),
        },
        key=settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, "HS256")
    except Exception as ex:
        print(ex)
        return None


def token_valid(token, user):
    payload = decode_token(token)
    if payload:
        email, exp = payload["email"], payload["exp"]
        datetime_exp: str = time.strftime("%H-%M", time.gmtime(exp))
        if (
            datetime.datetime.now().time()
            < datetime.datetime.strptime(datetime_exp, "%H-%M").time()
        ) and email != user.email:
            return True, payload
    return False


def send_change_email(user):
    mail = EmailMultiAlternatives(
        subject=f"Здравствуйте, {user.username}, измените свою почту!",
        body="",
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    token = encode_token(user)
    mail.attach_alternative(
        render_to_string(
            "email_change.html",
            context={
                "user": user,
                "link": (
                    settings.EMAIL_PAGE_DOMAIN + reverse("changed_email", args=[token])
                ),
            },
        ),
        "text/html",
    )
    mail.send()
