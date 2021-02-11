from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django_lab.settings import EMAIL_HOST_USER
from django_lab.celery import app

logger = get_task_logger(__name__)


@app.task
def send_confirmation_email(html, email):
    msg = EmailMultiAlternatives(
        subject="Подтвердите электронный адрес",
        body=html,
        from_email=EMAIL_HOST_USER,
        to=[email],
    )
    msg.content_subtype = 'html'
    logger.info(f'Message to {email} was sent')
    msg.send()
