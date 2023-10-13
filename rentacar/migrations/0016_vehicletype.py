# Generated by Django 4.2.5 on 2023-10-13 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0015_remove_car_number_of_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, verbose_name='Araç Tipi')),
            ],
            options={
                'verbose_name': 'Araç Tipi',
                'verbose_name_plural': 'Araç Tipleri',
                'ordering': ['type'],
            },
        ),
    ]