# Generated by Django 4.2 on 2023-09-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0018_apartment_other_rooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='other_rooms',
            field=models.JSONField(default=[]),
        ),
    ]
