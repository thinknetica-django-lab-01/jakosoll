FROM python:3.9-slim-buster

WORKDIR /usr/src/django_lab

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until

RUN apt-get update && apt-get install postgresql-server-dev-all gcc python3-dev musl-dev netcat -y

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/django_lab/requirements.txt

RUN pip install -r /usr/src/django_lab/requirements.txt

COPY . /usr/src/django_lab

COPY entrypoint.sh /usr/src/django_lab/entrypoint.sh

ENTRYPOINT ["/usr/src/django_lab/entrypoint.sh"]
