# Generated by Django 4.2 on 2023-05-28 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0032_alter_apartment_apartment_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="amenities",
            field=models.JSONField(blank=True, default="amenities:{}", null=True),
        ),
    ]