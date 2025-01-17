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
