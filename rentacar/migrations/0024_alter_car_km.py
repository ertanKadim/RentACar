# Generated by Django 4.2.5 on 2023-10-17 19:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0023_alter_car_plate_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='km',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Kilometre'),
        ),
    ]