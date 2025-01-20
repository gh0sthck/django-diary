# django-diary
A project in Django 5, which is a site for taking notes, that is, a diary (although the purpose of 
use depends on each person). The user can log in or register, but at the same time, without registering 
and having an account, the user cannot use any parts of the site. The data (note) of some users
are not available for viewing and modification by other users: each user has his own notes, can
edit and delete them, but cannot view the notes of other users.

## Tag-system
Each note can be tagged to indicate the intended topic and content of the entry. An note can
contain an unlimited number of tags, but cannot contain duplicates.

## App tech-stack
1. Python 3.12
2. Django 5
3. Django-MD-editor
4. Bootstrap 5
5. PostgreSQL 
6. Docker & Docker-Compose
7. Celery

# Project install
You need installed Python 3.12 and Docker on your computer. After git clone project, you should go
into `docker-compose.yaml` and change two variables: `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in
`celery` and `django` services.

This variables responsible to email address which send message (`EMAIL_HOST_USER`) and password from 
this email address (`EMAIL_HOST_PASSWORD`). But, `EMAIL_HOST_PASSWORD` *not* equal your `EMAIL_HOST_USER`
account! To get this password, you should go to Google settings in that account, find app passwords 
and create password to specific app.

In alternative, you can use other django-backend (e.g, for testing — console backend) or other email services. 

# Project start
For project start use:
```sh
docker-compose up
```

## Project setting
Before start work with project, you should migrate migrations to project. You can
use:
```sh
docker ps
```
to find `django` container and to know container name; after go into this container:
```sh 
docker exec -it <container_id> sh
```
in container execute:
```sh
python manage.py migrate
python manage.py createsuperuser
```
and Ctrl+C to exit. Last command create superuser.
