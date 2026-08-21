from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    all_products = Product.objects.filter(is_active=True)
    featured_products = all_products.filter(featured=True)[:8]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'all_products': all_products,
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
