# Generated by Django 3.1.1 on 2020-10-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0008_auto_20201018_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hackproject',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='hackproject',
            name='mentor',
        ),
        migrations.AlterField(
            model_name='hackproject',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
