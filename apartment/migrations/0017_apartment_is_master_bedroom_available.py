# Generated by Django 4.2 on 2023-09-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0016_remove_apartment_is_master_bedroom_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='is_master_bedroom_available',
            field=models.BooleanField(default=True),
        ),
    ]
