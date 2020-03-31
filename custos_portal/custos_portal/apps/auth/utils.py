from django.conf import settings
from django.core.mail import EmailMessage
from django.http.request import split_domain_port

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


def send_new_user_email(request, username, email, first_name, last_name):
    """Send new user email notification to portal admins."""
    new_user_email_template = models.EmailTemplate.objects.get(
        pk=models.NEW_USER_EMAIL_TEMPLATE)
    domain, port = split_domain_port(request.get_host())
    context = Context({
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "portal_title": settings.PORTAL_TITLE,
        "gateway_id": settings.GATEWAY_ID,
        "http_host": domain,
    })
    subject = Template(new_user_email_template.subject).render(context)
    body = Template(new_user_email_template.body).render(context)
    msg = EmailMessage(subject=subject,
                       body=body,
                       from_email="{} <{}>".format(
                           settings.PORTAL_TITLE,
                           settings.SERVER_EMAIL),
                       to=[a[1] for a in getattr(settings,
                                                 'PORTAL_ADMINS',
                                                 settings.ADMINS)])
    msg.content_subtype = 'html'
    msg.send()
