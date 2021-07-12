from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth import get_user_model


from ...common.models import BaseModelGeneric

User = get_user_model()

now = timezone.now()
upload_root = getattr(settings, "CHUNK_UPLOAD_FOLDER", "/srv/media/chunked/upload/")
finished_root = getattr(settings, "CHUNK_UPLOAD_FOLDER", "/srv/media/chunked/final/")


def upload_path():
    return upload_root


def final_path():
    return finished_root


private_storage = FileSystemStorage(location=final_path())


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


class ChunkedUpload(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128)
    folder = models.CharField(max_length=256)
    file = models.FileField(storage=private_storage, blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.filename
