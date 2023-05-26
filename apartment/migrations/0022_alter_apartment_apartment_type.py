# Generated by Django 4.2 on 2023-05-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0021_alter_apartment_amenities_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apartment",
            name="apartment_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Shared Housing", "Shared Housing"),
                    ("Credit Renting", "Credit Renting"),
                ],
                default="Shared Housing",
                null=True,
            ),
        ),
    ]