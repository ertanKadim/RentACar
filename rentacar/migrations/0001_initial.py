# Generated by Django 4.2.5 on 2023-09-23 13:20

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Kategori Adı')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategoriler',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100, verbose_name='Marka')),
                ('model', models.CharField(max_length=100, verbose_name='Model')),
                ('year', models.IntegerField(verbose_name='Yıl')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='get_slug', unique=True, verbose_name='Slug')),
                ('is_available', models.BooleanField(default=False, verbose_name='Kiralık Mı?')),
                ('is_damaged', models.BooleanField(default=False, verbose_name='Hasarlı Mı?')),
                ('km', models.IntegerField(verbose_name='Kilometre')),
                ('number_of_doors', models.CharField(max_length=2, verbose_name='Kapı Sayısı')),
                ('luggage_volume', models.CharField(max_length=50, verbose_name='Bagaj Hacmi')),
                ('fuel_type', models.CharField(max_length=50, verbose_name='Yakıt Türü')),
                ('transmission_type', models.CharField(max_length=50, verbose_name='Vites Türü')),
                ('color', models.CharField(max_length=50, verbose_name='Renk')),
                ('number_of_person', models.CharField(max_length=2, verbose_name='Kişi Sayısı')),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Günlük Fiyat')),
                ('pickup_location', models.CharField(max_length=255, null=True, verbose_name='Alış Yeri')),
                ('dropoff_location', models.CharField(max_length=255, null=True, verbose_name='Teslim Yeri')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Kiralanma Tarihi')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Kiralanma Saati')),
                ('return_date', models.DateField(blank=True, null=True, verbose_name='Teslim Tarihi')),
                ('return_time', models.TimeField(blank=True, null=True, verbose_name='Teslim Saati')),
                ('image1', models.URLField(blank=True, null=True, verbose_name='1. Fotoğrak Linki')),
                ('image2', models.URLField(blank=True, null=True, verbose_name='2. Fotoğrak Linki')),
                ('image3', models.URLField(blank=True, null=True, verbose_name='3. Fotoğrak Linki')),
                ('image4', models.URLField(blank=True, null=True, verbose_name='4. Fotoğrak Linki')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentacar.category', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Araba',
                'verbose_name_plural': 'Arabalar',
                'ordering': ['-id'],
            },
        ),
    ]
