# Generated by Django 4.2.2 on 2023-08-11 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_customuser_user_type_profile_profile_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isActiveHost',
            field=models.BooleanField(default=False),
        ),
    ]