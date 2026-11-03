from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),
    path('producto/<slug:slug>/', views.product_detail, name='product_detail'),
    path('consulta/', views.price_lookup, name='price_lookup'),
    path('consulta/sw.js', views.price_lookup_sw, name='price_lookup_sw'),
]
