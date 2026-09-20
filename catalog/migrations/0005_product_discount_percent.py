from django.db import migrations, models
from django.core.validators import MaxValueValidator, MinValueValidator


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_add_yerbas_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percent',
            field=models.PositiveIntegerField(
                default=0,
                validators=[MinValueValidator(0), MaxValueValidator(100)],
                verbose_name='descuento (%)',
            ),
        ),
    ]
