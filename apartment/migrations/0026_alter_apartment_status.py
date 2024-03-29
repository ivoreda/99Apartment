# Generated by Django 4.2 on 2023-10-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0025_alter_apartmentbooking_rooms_paid_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='status',
            field=models.CharField(choices=[('Listed', 'Listed'), ('Unlisted', 'Unlisted'), ('Pending', 'Pending'), ('Draft', 'Draft')], default='Unlisted', max_length=255),
        ),
    ]
