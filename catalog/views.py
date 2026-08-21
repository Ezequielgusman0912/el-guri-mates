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


def _shuffled_collage(images, repeats, min_distance):
    """Repeat and shuffle images so the same one never lands within
    `min_distance` cells of itself (avoids same-photo-next-door on the grid).

    Each repeat is a full shuffled permutation of `images` (so a photo never
    repeats within a single round), and only the boundary between rounds is
    checked against `min_distance` to avoid a near-repeat across the seam.
    """
    result = []
    for _ in range(repeats):
        tail = result[-min_distance:]
        for _ in range(500):
            round_images = images.copy()
            random.shuffle(round_images)
            candidate = tail + round_images
            if all(
                candidate[i] != candidate[j]
                for i in range(len(candidate))
                for j in range(i + 1, min(i + 1 + min_distance, len(candidate)))
            ):
                break
        result.extend(round_images)
    return result


def home(request):
    categories = Category.objects.all()
    all_products = Product.objects.filter(is_active=True)
    featured_products = all_products.filter(featured=True)[:8]
    collage_images = _shuffled_collage(HERO_COLLAGE_IMAGES, repeats=3, min_distance=5)
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
