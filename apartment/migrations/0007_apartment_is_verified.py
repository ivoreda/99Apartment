# Generated by Django 4.2 on 2023-08-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0006_remove_apartment_type_of_space'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
