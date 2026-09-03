from django.db import migrations


def add_varios_category(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Category.objects.get_or_create(
        slug='varios',
        defaults={'name': 'Varios', 'order': 4},
    )


def remove_varios_category(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Category.objects.filter(slug='varios').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_productimage'),
    ]

    operations = [
        migrations.RunPython(add_varios_category, remove_varios_category),
    ]
