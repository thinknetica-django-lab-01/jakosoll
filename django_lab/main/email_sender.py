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
