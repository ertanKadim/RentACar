# Generated by Django 4.2.5 on 2023-10-13 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0013_car_plate_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casetype',
            options={'ordering': ['type'], 'verbose_name': 'Kasa Tipi', 'verbose_name_plural': 'Kasa Tipleri'},
        ),
        migrations.AlterModelOptions(
            name='fueltype',
            options={'ordering': ['type'], 'verbose_name': 'Yakıt Türü', 'verbose_name_plural': 'Yakıt Türleri'},
        ),
        migrations.AlterModelOptions(
            name='transmissiontype',
            options={'ordering': ['type'], 'verbose_name': 'Vites Türü', 'verbose_name_plural': 'Vites Türleri'},
        ),
    ]
