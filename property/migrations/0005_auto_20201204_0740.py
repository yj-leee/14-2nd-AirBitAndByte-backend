# Generated by Django 3.1.3 on 2020-12-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20201204_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_per_guest',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
    ]
