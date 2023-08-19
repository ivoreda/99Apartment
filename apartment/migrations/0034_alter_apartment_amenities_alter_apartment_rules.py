# Generated by Django 4.2 on 2023-05-28 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0033_alter_apartment_amenities"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="amenities",
            field=models.JSONField(blank=True, default={"amenities": []}, null=True),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="rules",
            field=models.JSONField(blank=True, default={"rules": []}, null=True),
        ),
    ]