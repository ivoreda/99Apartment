# Generated by Django 4.2 on 2023-08-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0064_apartment_credit_renting_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaftyAndSecurity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='safty_and_security',
            field=models.JSONField(blank=True, default=[], null=True),
        ),
    ]
