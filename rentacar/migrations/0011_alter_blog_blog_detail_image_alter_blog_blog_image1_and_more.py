# Generated by Django 4.2.5 on 2023-12-23 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0010_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_detail_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Blog Detay Fotoğraf (1200x800)'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_image1',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Blog Fotoğraf (600x400)'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_recent_image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Sidebar Fotoğraf (400x400)'),
        ),
    ]