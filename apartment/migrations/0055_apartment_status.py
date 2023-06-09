# Generated by Django 4.2 on 2023-06-09 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0054_apartment_owner_id_apartment_owner_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartment",
            name="status",
            field=models.CharField(
                choices=[("Listed", "Listed"), ("Unlisted", "Unlisted")],
                default="Unlisted",
                max_length=255,
            ),
        ),
    ]