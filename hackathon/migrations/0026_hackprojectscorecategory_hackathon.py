# Generated by Django 3.1.3 on 2021-01-18 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon', '0025_auto_20210111_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackprojectscorecategory',
            name='hackathon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hackprojectscorecategories', to='hackathon.hackathon'),
        ),
    ]
