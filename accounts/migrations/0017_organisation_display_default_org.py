# Generated by Django 3.1.8 on 2021-07-27 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customuser_is_external'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='display_default_org',
            field=models.BooleanField(default=True, help_text="If set to True all users in this organisation will see their own and the default organisation's (pk=1) hackathons."),
        ),
    ]