from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product

from .cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from .utils import send_order_emails


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    cart.add(product, max(quantity, 1))
    messages.success(request, f'Agregaste {product.name} a tu pedido.')
    next_url = request.POST.get('next')
    return redirect(next_url or 'orders:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart})


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    cart.update(product, quantity)
    return redirect('orders:cart_detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('orders:cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, 'Tu pedido está vacío. Agregá productos antes de continuar.')
        return redirect('catalog:home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            order.order_number = f'EGM-{order.id:05d}'
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    unit_price=item['price'],
                    quantity=item['quantity'],
                )
            order.save()
            try:
                send_order_emails(order)
            except Exception as e:
                messages.warning(
                    request,
                    'Tu pedido se registró, pero hubo un problema enviando el email de '
                    f'confirmación. Te contactaremos igual. [DEBUG: {e!r}]',
                )
            cart.clear()
            return redirect('orders:order_success', order_number=order.order_number)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    message = quote(f'Hola! Soy {order.full_name}, quiero coordinar mi pedido {order.order_number} 🧉')
    whatsapp_order_url = f'https://wa.me/{settings.WHATSAPP_NUMBER}?text={message}'
    return render(request, 'orders/order_success.html', {
        'order': order,
        'whatsapp_order_url': whatsapp_order_url,
    })
