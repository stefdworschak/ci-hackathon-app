# Generated by Django 3.1.3 on 2021-02-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20210215_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('', 'Select Post Category'), ('participant', 'Participant'), ('mentor', 'Mentor'), ('staff', 'Staff'), ('admin', 'Admin')], default='participant', max_length=20),
        ),
    ]
