import random

from django.shortcuts import get_object_or_404, render

from .models import Category, Product


HERO_COLLAGE_IMAGES = [
    'img/hero-collage/hero-1.jpg',
    'img/hero-collage/hero-2.jpg',
    'img/hero-collage/hero-3.webp',
    'img/hero-collage/hero-4.webp',
    'img/hero-collage/hero-5.webp',
    'img/hero-collage/hero-6.webp',
    'img/hero-collage/hero-7.webp',
    'img/hero-collage/hero-8.jpg',
]


def home(request):
    categories = Category.objects.all()
    all_products = Product.objects.filter(is_active=True)
    featured_products = all_products.filter(featured=True)[:8]
    collage_images = HERO_COLLAGE_IMAGES * 6
    random.shuffle(collage_images)
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'all_products': all_products,
        'hero_collage_images': collage_images,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})
