# Generated by Django 4.2 on 2023-09-12 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0011_alter_apartment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='owner_price',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=10),
        ),
    ]
