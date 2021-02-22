from django.db import models


class TechnologyUsed(models.Model):
    """ A type of technology used as part of a Hackathon """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    display_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
