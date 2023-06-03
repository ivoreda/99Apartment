# Generated by Django 4.2 on 2023-06-02 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "apartment",
            "0046_rename_maintainance_category_maintainance_maintenance_category_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="apartmentbooking",
            name="cover_photo",
            field=models.TextField(default="photo"),
        ),
        migrations.AddField(
            model_name="apartmentbooking",
            name="email",
            field=models.EmailField(default="email", max_length=254),
        ),
        migrations.AddField(
            model_name="apartmentbooking",
            name="first_name",
            field=models.CharField(default="first name"),
        ),
        migrations.AddField(
            model_name="apartmentbooking",
            name="last_name",
            field=models.CharField(default="last name"),
        ),
        migrations.AddField(
            model_name="apartmentbooking",
            name="payment_link",
            field=models.CharField(default="payment link", max_length=255),
        ),
        migrations.AddField(
            model_name="apartmentbooking",
            name="phone_number",
            field=models.CharField(default="phone number"),
        ),
    ]
