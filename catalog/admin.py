from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'featured')
    list_filter = ('category', 'is_active', 'featured')
    list_editable = ('price', 'stock', 'is_active', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
