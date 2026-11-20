from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('nombre', max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.PositiveIntegerField('orden', default=0)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# Tipos y materiales de mate, en el orden en que se muestran en la página de Mates.
MATE_TIPO_CHOICES = [
    ('imperial', 'Imperial'),
    ('torpedo', 'Torpedo'),
    ('galleta', 'Galleta'),
    ('camionero', 'Camionero'),
    ('criollo', 'Criollo'),
    ('ranchero', 'Ranchero'),
    ('otros', 'Otros'),
]

MATE_MATERIAL_CHOICES = [
    ('calabaza', 'Calabaza'),
    ('algarrobo', 'Algarrobo'),
    ('acero', 'Acero'),
]

MATES_CATEGORY_SLUG = 'mates'


def guess_mate_tipo(name):
    """Adivina el tipo por el nombre. "Torpedo Imperial" es torpedo, por eso va primero."""
    n = name.lower()
    if 'torped' in n:
        return 'torpedo'
    if 'imperial' in n or 'roma' in n:
        return 'imperial'
    for tipo in ('galleta', 'camionero', 'criollo', 'ranchero'):
        if tipo in n:
            return tipo
    return 'otros'


def guess_mate_material(name, description=''):
    """Solo reconoce algarrobo; el acero en el nombre suele ser la virola, así que se elige a mano."""
    text = f'{name} {description[:400]}'.lower()
    return 'algarrobo' if 'algarrobo' in text else 'calabaza'


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, verbose_name='categoría'
    )
    tipo = models.CharField(
        'tipo de mate', max_length=20, choices=MATE_TIPO_CHOICES, blank=True,
        help_text='Solo para mates. Si lo dejás vacío se completa solo según el nombre.',
    )
    material = models.CharField(
        'material', max_length=20, choices=MATE_MATERIAL_CHOICES, blank=True,
        help_text='Solo para mates. Si lo dejás vacío se completa solo (algarrobo o calabaza).',
    )
    name = models.CharField('nombre', max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField('descripción', blank=True)
    price = models.DecimalField('precio original', max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(
        'descuento (%)',
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    stock = models.PositiveIntegerField('stock', default=0)
    image = models.ImageField('imagen', upload_to='productos/', blank=True, null=True)
    is_active = models.BooleanField('activo', default=True)
    featured = models.BooleanField('destacado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-featured', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f'{base}-{n}'
            self.slug = slug
        if self.category_id and self.category.slug == MATES_CATEGORY_SLUG:
            if not self.tipo:
                self.tipo = guess_mate_tipo(self.name)
            if not self.material:
                self.material = guess_mate_material(self.name, self.description)
        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def has_discount(self):
        return self.discount_percent > 0

    @property
    def discounted_price(self):
        if not self.has_discount:
            return self.price
        discount = Decimal(100 - self.discount_percent) / Decimal(100)
        return (self.price * discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def current_price(self):
        return self.discounted_price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField('imagen', upload_to='productos/galeria/')
    order = models.PositiveIntegerField('orden', default=0)

    class Meta:
        verbose_name = 'foto adicional'
        verbose_name_plural = 'fotos adicionales'
        ordering = ['order', 'id']

    def __str__(self):
        return f'Foto de {self.product.name}'
