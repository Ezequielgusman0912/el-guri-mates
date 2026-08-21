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


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, verbose_name='categoría'
    )
    name = models.CharField('nombre', max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    description = models.TextField('descripción', blank=True)
    price = models.DecimalField('precio', max_digits=10, decimal_places=2)
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
        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.stock > 0
