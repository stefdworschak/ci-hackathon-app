from django.db import models

from accounts.models import CustomUser as User
from .lists import INSTRUCTIONAL_CONTENT_CHOICES


class InstructionalContent(models.Model):
    """ Model representing instructional content for users such as videos
    text or hyperlinks """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name="instructional_content")
    display_name = models.CharField(default="", max_length=255, blank=False)
    description = models.TextField(
        blank=True, default="",
        help_text=("Description of the Instructional Content."))
    external_url = models.URLField(default="", max_length=255, blank=True,
        help_text=("For example, for an external video file."))
    is_active = models.BooleanField(default=True)
    content_type = models.CharField(default="text", max_length=255,
        choices=INSTRUCTIONAL_CONTENT_CHOICES)
    position = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Instructional Content'
        verbose_name_plural = 'Instructional Content'

    def __str__(self):
        return self.display_name
