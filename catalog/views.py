from django.db.models import Sum
from django.shortcuts import get_object_or_404, render

from orders.models import OrderItem

from .models import Category, Product


# Orden fijo para las ocho imágenes únicas de la grilla del hero.
HERO_COLLAGE_IMAGES = [
    'img/hero-collage/hero-6.webp',
    'img/hero-collage/hero-2.jpg',
    'img/hero-collage/hero-8.jpg',
    'img/hero-collage/hero-1.jpg',
    'img/hero-collage/hero-3.webp',
    'img/hero-collage/hero-5.webp',
    'img/hero-collage/hero-7.webp',
    'img/hero-collage/hero-4.webp',
]


CATEGORY_IMAGES = {
    'mates': {
        'image': 'img/categories/mates.webp',
        'position': 'center',
        'header_position': 'center 45%',
    },
    'bombillas': {'image': 'img/categories/bombillas.webp', 'position': 'center'},
    'canastas-materas': {'image': 'img/categories/canastas-materas.webp', 'position': 'center'},
    'termos': {
        'image': 'img/categories/termos.webp',
        'position': 'center 15%',
        'header_position': 'center 15%',
    },
    'varios': {
        'image': 'img/categories/8cd851095ba48fe486b987d247bbeb2949c178786d15b928b625f01ec95d519d385769.png',
        'position': 'center',
        'header_position': 'center',
    },
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
    category_data = CATEGORY_IMAGES.get(category.slug, {})
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
        'category_image': category_data.get('image'),
        'category_image_position': category_data.get(
            'header_position', category_data.get('position', 'center')
        ),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})
