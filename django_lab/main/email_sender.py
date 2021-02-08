from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django_lab.settings import EMAIL_HOST_USER


def send_greeting_email(user):
    template = loader.get_template(template_name='emails/greeting.html')
    html = template.render(context={'user': user})
    msg = EmailMultiAlternatives(
        subject="Приветствем на нашем сайте!",
        body=html,
        from_email=EMAIL_HOST_USER,
        to=[user.email],
    )
    msg.content_subtype = 'html'
    msg.send()


def send_new_goods_email(product, emails):
    template = loader.get_template(template_name='emails/goods_subscription.html')
    html = template.render(context={'product': product})
    msg = EmailMultiAlternatives(
        subject="Был добавлен новый товар",
        body=html,
        from_email=EMAIL_HOST_USER,
        to=emails,
    )
    msg.content_subtype = 'html'
    msg.send()
