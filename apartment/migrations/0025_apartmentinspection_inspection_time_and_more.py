# Generated by Django 4.2 on 2023-05-20 11:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("apartment", "0024_alter_apartmentbooking_end_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartmentinspection",
            name="inspection_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="apartmentinspection",
            name="inspection_date",
            field=models.DateField(),
        ),
    ]