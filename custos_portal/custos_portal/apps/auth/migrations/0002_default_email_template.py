from __future__ import unicode_literals

from django.db import migrations

from custos_portal.apps.auth.models import (
    NEW_USER_EMAIL_TEMPLATE,
    VERIFY_EMAIL_TEMPLATE
)


def default_templates(apps, schema_editor):

    EmailTemplate = apps.get_model("custos_portal_auth", "EmailTemplate")
    verify_email_template = EmailTemplate(
        template_type=VERIFY_EMAIL_TEMPLATE,
        subject="{{first_name}} {{last_name}} ({{username}}), "
                "Please Verify Your Email Account in {{portal_title}}",
        body="""
        <p>
        Dear {{first_name}} {{last_name}},
        </p>

        <p>
        Someone has created an account with this email address. If this was
        you, click the link below to verify your email address:
        </p>

        <p><a href="{{url}}">{{url}}</a></p>

        <p>If you didn't create this account, just ignore this message.</p>
        """.strip())
    verify_email_template.save()
    new_user_email_template = EmailTemplate(
        template_type=NEW_USER_EMAIL_TEMPLATE,
        subject="New User Account Was Created Successfully",
        body="""
        <p>Gateway Portal: {{http_host}}</p>
        <p>Tenant: {{gateway_id}}</p>
        <p>Username: {{username}}</p>
        <p>Name: {{first_name}} {{last_name}}</p>
        <p>Email: {{email}}</p>
        """.strip()
    )
    new_user_email_template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('custos_portal_auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(default_templates)
    ]