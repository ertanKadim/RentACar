# Generated by Django 4.2.5 on 2023-10-01 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentacar', '0007_caravailability'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CarAvailability',
        ),
    ]