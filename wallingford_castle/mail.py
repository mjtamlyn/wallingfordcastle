from django.conf import settings

from render_block import render_block_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail

api_client = SendGridAPIClient(settings.SENDGRID_API_KEY)


def send_mail(to_emails, template_name, context={}, from_email='hello@wallingfordcastle.co.uk'):
    template_name = 'templated_email/%s.email' % template_name
    subject = render_block_to_string(template_name, 'subject', context)
    plain_content = render_block_to_string(template_name, 'plain', context)
    html_content = render_block_to_string(template_name, 'html', context)
    message = Mail(
        from_email=From(from_email, 'Wallingford Castle Archers'),
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
        plain_text_content=plain_content,
    )
    if settings.SENDGRID_API_KEY:
        api_client.send(message)
    else:
        print(message)
