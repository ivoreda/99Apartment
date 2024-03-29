# Generated by Django 4.2 on 2023-09-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0020_apartment_master_bedroom_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartment',
            old_name='other_rooms',
            new_name='rooms',
        ),
        migrations.RenameField(
            model_name='apartmentbooking',
            old_name='no_of_guests',
            new_name='no_of_rooms',
        ),
        migrations.AddField(
            model_name='apartment',
            name='accommodation_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='apartment',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='single_room_total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='additionalcharge',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='map_url',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='master_bedroom_percentage',
            field=models.FloatField(default=0.3),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='master_bedroom_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='master_bedroom_tax_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='master_bedroom_total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='owner_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='tax',
            field=models.FloatField(default=7.5),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='tax_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='apartmentbooking',
            name='amount_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='service',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
