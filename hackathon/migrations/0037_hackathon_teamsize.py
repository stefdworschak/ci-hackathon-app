# Generated by Django 3.1.3 on 2021-02-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0036_remove_hackathon_judging_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='teamsize',
            field=models.IntegerField(default=3),
        ),
    ]
