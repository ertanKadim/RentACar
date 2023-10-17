# Generated by Django 4.2.5 on 2023-10-17 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0019_alter_car_price_per_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Oluşturulma Tarihi'),
        ),
        migrations.AddField(
            model_name='car',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Güncellenme Tarihi'),
        ),
    ]
