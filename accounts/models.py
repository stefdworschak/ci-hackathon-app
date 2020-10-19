from django.db import models
from django.contrib.auth.models import AbstractUser

"""List of user types to be passed into dropdown of same name for each 
user selection."""
USER_TYPE_CHOICES = [
    ('', 'Select Post Category'),
    ('participant', 'Participant'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
]

"""List of CI LMS modules to be passed into dropdown of same name for each 
user selection."""
LMS_MODULES_CHOICES = [
    ('', 'Select Learning Stage'),
    ('programme_preliminaries', 'Programme Preliminaries'),
    ('programming_paradigms', 'Programming Paradigms'),
    ('html_fundamentals', 'HTML Fundamentals'),
    ('css_fundamentals', 'CSS Fundamentals'),
    ('user_centric_frontend_development', 'User Centric Frontend Development'),
    ('javascript_fundamentals', 'Javascript Fundamentals'),
    ('interactive_frontend_development', 'Interactive Frontend Development'),
    ('python_fundamentals', 'Python Fundamentals'),
    ('practical_python', 'Practical Python'),
    ('data_centric_development', 'Data Centric Development'),
    ('full_stack_frameworks_with_django', 'Full Stack Frameworks with Django'),
    ('alumni', 'Alumni'),
    ('staff', 'Staff'),
]

class CustomUser(AbstractUser):
    slack_display_name = models.CharField(
        max_length=80,
        blank=False,
        null=True
    )
    user_type = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        choices=USER_TYPE_CHOICES
    )
    current_lms_module = models.CharField(
        max_length=35,
        blank=False,
        null=True,
        choices=LMS_MODULES_CHOICES
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
