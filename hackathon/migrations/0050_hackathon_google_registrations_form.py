# Generated by Django 3.1.13 on 2024-09-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0049_hackathon_is_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='google_registrations_form',
            field=models.URLField(blank=True, default='', help_text='Link to the Google Form for registrations.'),
        ),
    ]