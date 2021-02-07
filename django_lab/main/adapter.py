from allauth.account.adapter import DefaultAccountAdapter
from django.core.mail import EmailMultiAlternatives
from django.template import loader


class CustomAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        template = loader.get_template(template_name='account/email/email_confirmation_message.html')
        html = template.render(context=context)
        msg = EmailMultiAlternatives(
            subject="Подтвердите электронный адрес",
            body=html,
            from_email='jako.soll@gmail.com',
            to=[email],
        )
        msg.content_subtype = 'html'
        print(f'Message to {email} was sent')
        msg.send()
