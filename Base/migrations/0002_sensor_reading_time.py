# Generated by Django 5.1.3 on 2025-03-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor_reading',
            name='time',
            field=models.DateTimeField(null=True),
        ),
    ]
