from django.db import migrations


def add_yerbas_category(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Category.objects.get_or_create(
        slug='yerbas',
        defaults={'name': 'Yerbas', 'order': 5},
    )


def remove_yerbas_category(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Category.objects.filter(slug='yerbas').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_add_varios_category'),
    ]

    operations = [
        migrations.RunPython(add_yerbas_category, remove_yerbas_category),
    ]
