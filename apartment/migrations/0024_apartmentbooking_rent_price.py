# Generated by Django 4.2 on 2023-10-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0023_alter_apartmentbooking_rooms_paid_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentbooking',
            name='rent_price',
            field=models.IntegerField(default=0),
        ),
    ]