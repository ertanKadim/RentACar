# Generated by Django 4.2.5 on 2023-10-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0022_alter_car_km_alter_car_luggage_volume_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='plate_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='Plaka Numarası'),
        ),
    ]