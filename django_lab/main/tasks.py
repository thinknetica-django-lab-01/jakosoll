from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django_lab.celery import app
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django_lab.settings import EMAIL_HOST_USER
from .models import Product, ProductSubscriber
from django.utils import timezone

EMAILS_UPDATE_SUBJECT = 'Обновления товаров за последние 7 дней'

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


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(
            minute='05',
            hour='17',
            day_of_week='friday'
        ),
        send_weeks_update.s(),
        name='Emails update every week'
    )


@app.task
def send_weeks_update():
    current_date = timezone.now()
    week_ago = current_date - timezone.timedelta(days=7)
    two_weeks_ago = current_date - timezone.timedelta(days=14)
    subscribers_qs = ProductSubscriber.objects.all()
    emails = [item.user.email for item in subscribers_qs]
    products_qs = Product.objects.filter(created__gte=two_weeks_ago, created__lte=week_ago)
    _send_new_goods_email(products_qs, EMAILS_UPDATE_SUBJECT, emails)
    print('Goods update was sent')


def _send_new_goods_email(products, subject, emails):
    template = loader.get_template(template_name='emails/goods_subscription.html')
    html = template.render(context={'products': products})
    msg = EmailMultiAlternatives(
        subject=subject,
        body=html,
        from_email=EMAIL_HOST_USER,
        to=emails,
    )
    msg.content_subtype = 'html'
    msg.send()
