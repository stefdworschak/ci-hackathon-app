# Generated by Django 3.1.3 on 2021-01-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201026_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='current_lms_module',
            field=models.CharField(choices=[
                ('', 'Select Learning Stage'),
                ('programme_preliminaries', 'Programme Preliminaries'),
                ('programming_paradigms', 'Programming Paradigms'),
                ('html_essentials', 'HTML Essentials'),
                ('css_essentials', 'CSS Essentials'),
                ('user_centric_frontend_development',
                 'User Centric Frontend Development'),
                ('comparative_programming_languages_essentials',
                 'Comparative Programming Languages Essentials'),
                ('javascript_essentials', 'Javascript Essentials'),
                ('interactive_frontend_development',
                 'Interactive Frontend Development'),
                ('python_essentials', 'Python essentials'),
                ('practical_python', 'Practical Python'),
                ('data_centric_development', 'Data Centric Development'),
                ('backend_development', 'Backend Development'),
                ('full_stack_frameworks_with_django',
                 'Full Stack Frameworks with Django'),
                ('alumni', 'Alumni'),
                ('staff', 'Staff')], default='', max_length=50),
        ),
    ]
