# Generated by Django 3.1.13 on 2024-09-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0048_auto_20221219_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='is_register',
            field=models.BooleanField(default=True),
        ),
    ]
