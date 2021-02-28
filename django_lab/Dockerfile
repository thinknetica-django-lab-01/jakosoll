FROM python:3.9-slim-buster

WORKDIR /usr/src/django_lab

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install postgresql-server-dev-all gcc python3-dev musl-dev -y

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/requirements.txt

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/django_lab
