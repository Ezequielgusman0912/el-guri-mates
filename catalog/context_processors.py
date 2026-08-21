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
        'nav_categories': Category.objects.all(),
        'cart_count': len(cart),
    }
