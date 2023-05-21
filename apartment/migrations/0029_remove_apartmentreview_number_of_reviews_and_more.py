# Generated by Django 4.2 on 2023-05-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0028_apartmentreview_number_of_reviews"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="apartmentreview",
            name="number_of_reviews",
        ),
        migrations.AddField(
            model_name="apartment",
            name="number_of_reviews",
            field=models.IntegerField(default=0),
        ),
    ]
