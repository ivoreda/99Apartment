# Generated by Django 4.2 on 2023-08-15 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0062_rules_apartment_cancellation_policy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Amenities',
            new_name='ApartmentAmenities',
        ),
        migrations.RenameModel(
            old_name='Rules',
            new_name='ApartmentRules',
        ),
    ]