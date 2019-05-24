
# Django Module
from django.db import models

from ...common.models import BaseModelGeneric


class ResizeImageTemp(BaseModelGeneric):
    image = models.URLField(max_length=300)
    is_done = models.BooleanField(default=False)
    is_progress = models.BooleanField(default=False)
    purpose = models.CharField(max_length=100)

    def __str__(self):
        return self.image

    class Meta:
        verbose_name = "Resize Image Temp"
        verbose_name_plural = "Resize Image Temps"
