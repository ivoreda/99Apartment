# Generated by Django 4.2 on 2023-10-09 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0021_rename_other_rooms_apartment_rooms_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentbooking',
            name='rooms_paid_for',
            field=models.JSONField(default=[]),
        ),
    ]
