# Generated by Django 4.2 on 2023-04-26 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0003_apartmentimages_created_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartmentinspection",
            name="isInspected",
            field=models.BooleanField(default=False),
        ),
    ]