# Generated by Django 4.2 on 2023-05-20 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0023_alter_apartment_map_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartmentbooking",
            name="end_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="apartmentbooking",
            name="start_date",
            field=models.DateField(),
        ),
    ]