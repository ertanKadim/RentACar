# Generated by Django 4.2.5 on 2023-12-16 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0004_booking_orderid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={},
        ),
        migrations.AlterField(
            model_name='booking',
            name='orderid',
            field=models.CharField(editable=False, max_length=9, unique=True, verbose_name='Sipariş ID'),
        ),
    ]
