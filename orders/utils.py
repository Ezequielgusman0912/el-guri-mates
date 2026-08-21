from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_emails(order):
    context = {
        'order': order,
        'items': order.items.all(),
        'site_name': settings.SITE_NAME,
    }

    customer_subject = f'Confirmación de tu pedido {order.order_number} - {settings.SITE_NAME}'
    customer_body = render_to_string('emails/order_customer.txt', context)
    send_mail(customer_subject, customer_body, settings.DEFAULT_FROM_EMAIL, [order.email], fail_silently=False)

    if settings.OWNER_EMAIL:
        owner_subject = f'Nuevo pedido {order.order_number}'
        owner_body = render_to_string('emails/order_owner.txt', context)
        send_mail(owner_subject, owner_body, settings.DEFAULT_FROM_EMAIL, [settings.OWNER_EMAIL], fail_silently=False)
