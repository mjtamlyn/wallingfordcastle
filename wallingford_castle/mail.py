from django.conf import settings

from mailgun.client import Client
from render_block import render_block_to_string

domain = settings.MAILGUN_DOMAIN
if settings.MAILGUN_API_KEY:
    api_client = Client(auth=('api', settings.MAILGUN_API_KEY))
else:
    api_client = None


def send_mail(to_emails, template_name, context={}, from_email=None):
    template_name = 'templated_email/%s.email' % template_name
    subject = render_block_to_string(template_name, 'subject', context)
    plain_content = render_block_to_string(template_name, 'plain', context)
    html_content = render_block_to_string(template_name, 'html', context)
    message = {
        'from': from_email or 'Wallingford Castle Archers <hello@wallingfordcastle.co.uk>',
        'to': to_emails,
        'subject': subject,
        'text': plain_content,
        'html': html_content,
    }
    if api_client:
        api_client.messages.create(data=message, domain=domain)
    else:
        print(message)
