# Generated by Django 4.2 on 2023-09-13 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0015_alter_apartment_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='is_master_bedroom_available',
        ),
    ]