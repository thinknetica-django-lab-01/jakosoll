from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_email(user):
    template = loader.get_template(template_name='greeting.html')
    html = template.render(context={'user': user})
    msg = EmailMultiAlternatives(
        subject="Приветствем на нашем сайте!",
        body=html,
        from_email='jako.soll@gmail.com',
        to=[user.email],
    )
    msg.content_subtype = 'html'
    msg.send()
