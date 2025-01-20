FROM python:3.12-alpine

WORKDIR /diary/

COPY requirements.txt /diary/

RUN [ "pip", "install", "-r", "requirements.txt" ]

COPY . /diary/

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
