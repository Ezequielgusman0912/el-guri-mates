from django.core.management.base import BaseCommand

from catalog.models import Category

CATEGORIES = ['Mates', 'Bombillas', 'Canastas Materas', 'Termos']


class Command(BaseCommand):
    help = 'Crea las categorías base de El Guri Mates si no existen'

    def handle(self, *args, **options):
        for i, name in enumerate(CATEGORIES):
            obj, created = Category.objects.get_or_create(name=name, defaults={'order': i})
            status = 'creada' if created else 'ya existía'
            self.stdout.write(self.style.SUCCESS(f'{name}: {status}'))
