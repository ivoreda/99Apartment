# Generated by Django 4.2 on 2023-10-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0022_apartmentbooking_rooms_paid_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentbooking',
            name='rooms_paid_for',
            field=models.JSONField(),
        ),
    ]
