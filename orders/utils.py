from email.mime.image import MIMEImage
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string


LOGO_PATH = Path(settings.BASE_DIR) / 'static' / 'img' / 'logo.png'
LOGO_CID = 'logo'


def send_order_emails(order):
    context = {
        'order': order,
        'items': order.items.all(),
        'site_name': settings.SITE_NAME,
        'logo_cid': LOGO_CID,
    }

    customer_subject = f'Confirmación de tu pedido {order.order_number} - {settings.SITE_NAME}'
    customer_text_body = render_to_string('emails/order_customer.txt', context)
    customer_email = EmailMultiAlternatives(
        customer_subject, customer_text_body, settings.DEFAULT_FROM_EMAIL, [order.email]
    )
    if LOGO_PATH.exists():
        customer_html_body = render_to_string('emails/order_customer.html', context)
        customer_email.attach_alternative(customer_html_body, 'text/html')
        customer_email.mixed_subtype = 'related'
        with open(LOGO_PATH, 'rb') as logo_file:
            logo_image = MIMEImage(logo_file.read())
            logo_image.add_header('Content-ID', f'<{LOGO_CID}>')
            logo_image.add_header('Content-Disposition', 'inline', filename='logo.png')
            customer_email.attach(logo_image)
    customer_email.send(fail_silently=False)

    if settings.OWNER_EMAIL:
        owner_subject = f'Nuevo pedido {order.order_number}'
        owner_body = render_to_string('emails/order_owner.txt', context)
        send_mail(owner_subject, owner_body, settings.DEFAULT_FROM_EMAIL, [settings.OWNER_EMAIL], fail_silently=False)
