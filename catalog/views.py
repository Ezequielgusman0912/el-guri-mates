from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from orders.models import OrderItem

from .models import Category, Product


# Orden fijo (no se recalcula por request) armado para que ninguna foto
# quede en un casillero adyacente a si misma en la grilla del hero.
HERO_COLLAGE_IMAGES = [
    'img/hero-collage/hero-6.webp',
    'img/hero-collage/hero-2.jpg',
    'img/hero-collage/hero-8.jpg',
    'img/hero-collage/hero-1.jpg',
    'img/hero-collage/hero-3.webp',
    'img/hero-collage/hero-5.webp',
    'img/hero-collage/hero-7.webp',
    'img/hero-collage/hero-4.webp',
    'img/hero-collage/hero-8.jpg',
    'img/hero-collage/hero-6.webp',
    'img/hero-collage/hero-2.jpg',
    'img/hero-collage/hero-3.webp',
    'img/hero-collage/hero-1.jpg',
    'img/hero-collage/hero-7.webp',
    'img/hero-collage/hero-4.webp',
    'img/hero-collage/hero-5.webp',
    'img/hero-collage/hero-6.webp',
    'img/hero-collage/hero-2.jpg',
    'img/hero-collage/hero-8.jpg',
    'img/hero-collage/hero-7.webp',
    'img/hero-collage/hero-1.jpg',
    'img/hero-collage/hero-4.webp',
    'img/hero-collage/hero-3.webp',
    'img/hero-collage/hero-5.webp',
]


CATEGORY_IMAGES = {
    'mates': {'image': 'img/categories/mates.webp', 'position': 'center'},
    'bombillas': {'image': 'img/categories/bombillas.webp', 'position': 'center'},
    'canastas-materas': {'image': 'img/categories/canastas-materas.webp', 'position': 'center'},
    'termos': {'image': 'img/categories/termos.webp', 'position': 'center 15%'},
}


def home(request):
    categories = Category.objects.all()
    products_qs = Product.objects.filter(is_active=True)
    featured_products = products_qs.filter(featured=True)[:8]

    sales_by_product = dict(
        OrderItem.objects
        .exclude(order__status='cancelado')
        .values('product_id')
        .annotate(total_sold=Sum('quantity'))
        .values_list('product_id', 'total_sold')
    )
    top_products = sorted(
        products_qs, key=lambda p: (-sales_by_product.get(p.id, 0), p.name)
    )[:4]

    categories_with_images = [
        {'category': cat, **CATEGORY_IMAGES.get(cat.slug, {'image': None, 'position': 'center'})}
        for cat in categories
    ]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'categories_with_images': categories_with_images,
        'featured_products': featured_products,
        'top_products': top_products,
        'hero_collage_images': HERO_COLLAGE_IMAGES,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
        'category_image': CATEGORY_IMAGES.get(category.slug, {}).get('image'),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})
