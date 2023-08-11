# Generated by Django 4.2.2 on 2023-08-11 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='BecomeAHostNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
