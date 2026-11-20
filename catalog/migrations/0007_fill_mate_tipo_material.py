"""Completa tipo y material de los mates que ya estaban cargados.

La lógica está copiada acá (y no importada de models.py) para que la migración
haga siempre lo mismo aunque las reglas cambien más adelante.
"""
from django.db import migrations


def guess_tipo(name):
    n = name.lower()
    if 'torped' in n:
        return 'torpedo'
    if 'imperial' in n or 'roma' in n:
        return 'imperial'
    for tipo in ('galleta', 'camionero', 'criollo', 'ranchero'):
        if tipo in n:
            return tipo
    return 'otros'


def guess_material(name, description):
    text = f'{name} {(description or "")[:400]}'.lower()
    if 'algarrobo' in text:
        return 'algarrobo'
    # El Torpedo Deluxe es el único con interior de acero (el "Acero" del Super Imperial es la virola).
    if 'torpedo deluxe' in name.lower():
        return 'acero'
    return 'calabaza'


def fill(apps, schema_editor):
    Product = apps.get_model('catalog', 'Product')
    for product in Product.objects.filter(category__slug='mates'):
        changed = []
        if not product.tipo:
            product.tipo = guess_tipo(product.name)
            changed.append('tipo')
        if not product.material:
            product.material = guess_material(product.name, product.description)
            changed.append('material')
        if changed:
            product.save(update_fields=changed)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_tipo_material'),
    ]

    operations = [
        migrations.RunPython(fill, migrations.RunPython.noop),
    ]
