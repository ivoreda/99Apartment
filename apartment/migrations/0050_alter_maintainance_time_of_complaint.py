# Generated by Django 4.2 on 2023-06-05 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0049_maintainance_apartment_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="maintainance",
            name="time_of_complaint",
            field=models.TimeField(auto_now_add=True),
        ),
    ]
