from django.conf import settings
from django.core.mail import EmailMessage

from . import models
from django.template import Context, Template


def send_email_to_user(template_id, context):
    email_template = models.EmailTemplate.objects.get(pk=template_id)
    subject = Template(email_template.subject).render(context)
    body = Template(email_template.body).render(context)
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email="\"{}\" <{}>".format(settings.PORTAL_TITLE,
                                        settings.SERVER_EMAIL),
        to=["\"{} {}\" <{}>".format(context['first_name'],
                                    context['last_name'],
                                    context['email'])],
        reply_to=[f"\"{a[0]}\" <{a[1]}>" for a in getattr(settings,
                                                          'PORTAL_ADMINS',
                                                          settings.ADMINS)]
    )
    msg.content_subtype = 'html'
    msg.send()
