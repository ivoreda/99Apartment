# Generated by Django 4.2 on 2023-09-12 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0013_remove_apartment_verification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='status',
            field=models.CharField(choices=[('Listed', 'Listed'), ('Unlisted', 'Unlisted'), ('Pending', 'Pending'), ('Draft', 'Draft')], default='Unverified', max_length=255),
        ),
    ]
