# Generated by Django 4.2 on 2023-05-30 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "apartment",
            "0035_apartmentimage_maintainance_remove_apartment_image1_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="maintainance",
            name="cost",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="maintainance",
            name="maintainance_category",
            field=models.CharField(
                choices=[("Routine", "Routine"), ("Emergency", "Emergency")],
                default="Routine",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="maintainance",
            name="maintainance_type",
            field=models.CharField(
                choices=[("Electrical", "Electrical"), ("Structural", "Structural")],
                default="Structural",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="maintainance",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Done", "Done")], max_length=20
            ),
        ),
    ]