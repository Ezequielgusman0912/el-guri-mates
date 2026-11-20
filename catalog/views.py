from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import MATE_MATERIAL_CHOICES, MATE_TIPO_CHOICES, Category, Product


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
    'yerbas': {
        'image': 'img/categories/yerbas.jpeg',
        'position': 'center',
        'header_position': 'center',
    },
}


def home(request):
    # Con annotate+GROUP BY Django ignora Meta.ordering, así que se ordena explícito.
    categories = Category.objects.annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).order_by('order', 'name')
    products_qs = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .prefetch_related('gallery')
    )
    offers_products = products_qs.filter(discount_percent__gt=0)[:8]
    new_products = products_qs.filter(stock__gt=0).order_by('-created_at')[:10]

    categories_with_images = [
        {'category': cat, **CATEGORY_IMAGES.get(cat.slug, {'image': None, 'position': 'center'})}
        for cat in categories
    ]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'categories_with_images': categories_with_images,
        'offers_products': offers_products,
        'new_products': new_products,
        'hero_collage_images': HERO_COLLAGE_IMAGES,
    })


# Título y frase de cada grupo en la página de Mates.
MATE_TIPO_INFO = {
    'todos': ('Todos los mates', 'Toda la colección de mates. Elegí un tipo arriba para ver solo esos.'),
    'imperial': ('Imperiales', 'El clásico de lujo, con virola y base de alpaca o acero.'),
    'torpedo': ('Torpedos', 'Cuerpo redondeado que se afina hacia la base. Cómodo en la mano.'),
    'galleta': ('Galletas', 'Forma baja y redondeada, un clásico que nunca falla.'),
    'camionero': ('Camioneros', 'Mates grandes, con presencia, para cebar largo.'),
    'criollo': ('Criollos', 'Calabaza natural, cuero y costura a mano, como se hizo siempre.'),
    'ranchero': ('Rancheros', 'Cuerpo alto y facetado, tallado en algarrobo.'),
    'otros': ('Otros mates', 'Uruguayo, Porito y otras piezas únicas.'),
}


def _filter_thumb(products):
    """Foto chica del primer mate con foto, prefiriendo los que tienen stock."""
    with_image = [p for p in products if p.image]
    if not with_image:
        return None
    best = next((p for p in with_image if p.in_stock), with_image[0])
    # Recorte automático con zoom medio: el mate llena el círculo en vez de perderse en la pared.
    return _cloudinary_thumb(best.image.url, 168, crop='c_thumb,g_auto,z_0.5')


def _mate_filters(products):
    """Botones de tipo y material; vacío si los productos no tienen tipo cargado."""
    if not any(p.tipo for p in products):
        return [], []
    by_tipo = {}
    for p in products:
        by_tipo.setdefault(p.tipo or 'otros', []).append(p)

    tipos = []
    for key, label in MATE_TIPO_CHOICES:
        group = by_tipo.get(key)
        if not group:
            continue
        title, desc = MATE_TIPO_INFO.get(key, (label, ''))
        thumb = _filter_thumb(group)
        tipos.append({
            'id': key, 'name': label, 'title': title, 'desc': desc,
            'count': len(group), 'images': [thumb] if thumb else [],
        })

    collage = [img for t in tipos[:4] for img in t['images']]
    title, desc = MATE_TIPO_INFO['todos']
    tipos.insert(0, {
        'id': 'todos', 'name': 'Todos', 'title': title, 'desc': desc,
        'count': len(products), 'images': collage, 'collage': len(collage) == 4,
    })

    materiales = [{'id': 'todos', 'name': 'Todos', 'count': len(products)}]
    for key, label in MATE_MATERIAL_CHOICES:
        count = sum(1 for p in products if p.material == key)
        materiales.append({'id': key, 'name': label, 'count': count})
    return tipos, materiales


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = list(category.products.filter(is_active=True).prefetch_related('gallery'))
    category_data = CATEGORY_IMAGES.get(category.slug, {})
    tipo_filters, material_filters = _mate_filters(products)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products,
        'tipo_filters': tipo_filters,
        'material_filters': material_filters,
        'category_image': category_data.get('image'),
        'category_image_position': category_data.get(
            'header_position', category_data.get('position', 'center')
        ),
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def _cloudinary_thumb(url, size, crop='c_fill'):
    """Pide a Cloudinary una versión chica de la foto; las URLs locales quedan igual."""
    if '/image/upload/' not in url:
        return url
    return url.replace('/image/upload/', f'/image/upload/{crop},w_{size},h_{size},f_auto,q_auto/', 1)


@staff_member_required
def price_lookup(request):
    """Consulta rápida de precios y stock para usar desde el celular mientras se vende."""
    products = Product.objects.select_related('category').order_by('name')
    items = [
        {
            'product': p,
            'thumb': _cloudinary_thumb(p.image.url, 160) if p.image else None,
            'large': _cloudinary_thumb(p.image.url, 700) if p.image else None,
        }
        for p in products
    ]
    categories = Category.objects.filter(products__isnull=False).distinct().order_by('order', 'name')
    return render(request, 'catalog/price_lookup.html', {'items': items, 'categories': categories})


# Service worker for the price lookup: it has to be served from /consulta/ so its scope covers the page.
# The page is fetched from the network first (fresh prices) and falls back to the last saved copy when
# there is no signal (e.g. at a fair); photos are kept once seen.
PRICE_LOOKUP_SW = """
const CACHE = 'consulta-v1';
self.addEventListener('install', (e) => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then((res) => {
      if (res.ok && !res.redirected) caches.open(CACHE).then((c) => c.put(req, res.clone()));
      return res.clone();
    }).catch(() => caches.match(req)));
  } else if (req.destination === 'image') {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      caches.open(CACHE).then((c) => c.put(req, res.clone()));
      return res.clone();
    })));
  }
});
"""


def price_lookup_sw(request):
    response = HttpResponse(PRICE_LOOKUP_SW, content_type='application/javascript')
    response['Cache-Control'] = 'no-cache'
    return response
