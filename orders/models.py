from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    order_number = models.CharField('número de pedido', max_length=20, unique=True, blank=True)
    full_name = models.CharField('nombre completo', max_length=150)
    email = models.EmailField('email')
    phone = models.CharField('teléfono', max_length=30)
    address = models.CharField('dirección', max_length=255, blank=True)
    notes = models.TextField('notas', blank=True)
    status = models.CharField('estado', max_length=20, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField('fecha', auto_now_add=True)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number or f'Pedido #{self.pk}'

    @property
    def total(self):
        return sum((item.subtotal for item in self.items.all()), 0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'catalog.Product', related_name='+', on_delete=models.SET_NULL, null=True, blank=True
    )
    product_name = models.CharField(max_length=150)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product_name}'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
