# Generated by Django 3.1.3 on 2021-01-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0028_auto_20210116_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hackproject',
            name='project_image_url',
        ),
        migrations.RemoveField(
            model_name='hackproject',
            name='screenshot_url',
        ),
        migrations.RemoveField(
            model_name='hackteam',
            name='header_image_url',
        ),
        migrations.AddField(
            model_name='hackproject',
            name='project_image',
            field=models.TextField(blank=True, default='', help_text="Image displayed next to the project on the team's page."),
        ),
        migrations.AddField(
            model_name='hackproject',
            name='screenshot',
            field=models.TextField(blank=True, default='', help_text="Project screenshot displayed on the team's page underneath the project information"),
        ),
        migrations.AddField(
            model_name='hackteam',
            name='header_image',
            field=models.TextField(blank=True, default='', help_text="Image displayed at the top of the team's page."),
        ),
    ]
