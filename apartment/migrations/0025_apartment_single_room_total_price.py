# Generated by Django 4.2 on 2023-09-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0024_rename_other_rooms_apartment_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='single_room_total_price',
            field=models.IntegerField(default=0),
        ),
    ]