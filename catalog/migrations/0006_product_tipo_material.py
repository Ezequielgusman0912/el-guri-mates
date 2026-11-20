from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_discount_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tipo',
            field=models.CharField(
                blank=True,
                choices=[
                    ('imperial', 'Imperial'), ('torpedo', 'Torpedo'), ('galleta', 'Galleta'),
                    ('camionero', 'Camionero'), ('criollo', 'Criollo'), ('ranchero', 'Ranchero'),
                    ('otros', 'Otros'),
                ],
                help_text='Solo para mates. Si lo dejás vacío se completa solo según el nombre.',
                max_length=20,
                verbose_name='tipo de mate',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(
                blank=True,
                choices=[('calabaza', 'Calabaza'), ('algarrobo', 'Algarrobo'), ('acero', 'Acero')],
                help_text='Solo para mates. Si lo dejás vacío se completa solo (algarrobo o calabaza).',
                max_length=20,
                verbose_name='material',
            ),
        ),
    ]
