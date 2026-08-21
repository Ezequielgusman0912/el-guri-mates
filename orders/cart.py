from decimal import Decimal

from catalog.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """Carrito de compras basado en la sesión del navegador."""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        pid = str(product.id)
        if pid in self.cart:
            self.cart[pid]['quantity'] += quantity
        else:
            self.cart[pid] = {'quantity': quantity, 'price': str(product.price)}
        self.save()

    def update(self, product, quantity):
        pid = str(product.id)
        if pid not in self.cart:
            return
        if quantity <= 0:
            self.remove(product)
        else:
            self.cart[pid]['quantity'] = quantity
            self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        for pid, item in self.cart.items():
            product = products.get(pid)
            if not product:
                continue
            price = Decimal(item['price'])
            quantity = item['quantity']
            yield {
                'product': product,
                'price': price,
                'quantity': quantity,
                'subtotal': price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total(self):
        return sum((Decimal(item['price']) * item['quantity'] for item in self.cart.values()), Decimal('0'))
