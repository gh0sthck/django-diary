from celery import shared_task
from django_email_verification import send_email, send_password

from users.models import DiaryUser
from .utils import send_change_email


@shared_task
def celery_send_email(user_id: int):
    user = DiaryUser.objects.get(id=user_id)
    send_email(user)
    

@shared_task
def celery_send_password(user_id: int):
    user = DiaryUser.objects.get(id=user_id)
    send_password(user)


@shared_task 
def celery_send_change_email(user_id: int):
    user = DiaryUser.objects.get(id=user_id)
    send_change_email(user)
