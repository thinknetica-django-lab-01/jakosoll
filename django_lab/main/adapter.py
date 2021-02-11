from allauth.account.adapter import DefaultAccountAdapter
from django.template import loader
from .tasks import send_confirmation_email


class CustomAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        template = loader.get_template(template_name='account/email/email_confirmation_message.html')
        html = template.render(context=context)
        send_confirmation_email.delay(html, email)
