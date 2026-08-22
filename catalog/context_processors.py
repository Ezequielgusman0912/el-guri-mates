from urllib.parse import quote

from django.conf import settings

from orders.cart import Cart

from .models import Category


def site_context(request):
    cart = Cart(request)
    message = quote('¡Hola! Quiero consultar sobre sus productos materos 🧉')
    whatsapp_url = f'https://wa.me/{settings.WHATSAPP_NUMBER}?text={message}'
    return {
        'site_name': settings.SITE_NAME,
        'whatsapp_url': whatsapp_url,
        'instagram_url': f'https://instagram.com/{settings.INSTAGRAM_USERNAME}',
        'instagram_username': settings.INSTAGRAM_USERNAME,
        'payment_methods': settings.PAYMENT_METHODS,
        'nav_categories': Category.objects.all(),
        'cart_count': len(cart),
        'debug': settings.DEBUG,
    }
