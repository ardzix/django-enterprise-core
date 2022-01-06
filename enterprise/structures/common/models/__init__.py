import json
from urllib.parse import unquote

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

from enterprise.libs.moment import to_timestamp
from enterprise.libs import storage
from enterprise.libs.model import BaseModelGeneric


User = settings.AUTH_USER_MODEL

GCS_BASE_URL = getattr(settings, 'GCS_BASE_URL', '')
RACKSPACE_BASE_URL = getattr(settings, 'RACKSPACE_BASE_URL', '')
USE_GCS = getattr(settings, 'USE_GCS', False)
USE_RACKSPACE = getattr(settings, 'USE_RACKSPACE', False)

# Create your models here.


class Log(models.Model):
    content_type = models.ForeignKey(ContentType,
                                     related_name="%(app_label)s_%(class)s_content_type",
                                     blank=True, null=True, on_delete=models.CASCADE,)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    logged_at = models.DateTimeField(blank=True, null=True)
    logged_at_timestamp = models.PositiveIntegerField(blank=True, null=True)
    logged_by = models.ForeignKey(
        User, db_index=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.logged_by.__str__()

    def get_message_dict(self):
        try:
            return json.loads(self.message)
        except BaseException:
            return {}

    def get_note(self):
        message_dict = self.get_message_dict()
        if "note" in message_dict:
            return message_dict['note']
        else:
            return "-"

    def save(self, *args, **kwargs):
        self.logged_at = timezone.now()
        self.logged_at_timestamp = to_timestamp(self.logged_at)

        return super(Log, self).save(*args, **kwargs)

    def read(self, *args, **kwargs):
        self.read_at = timezone.now()
        self.read_at_timestamp = to_timestamp(self.read_at)

        return self.save(*args, **kwargs)

    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")


class APILog(models.Model):
    """
    For API log each call, each user
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    app_id = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=100)
    request_method = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.app_id

    class Meta:
        verbose_name = _("APILog")
        verbose_name_plural = _("APILogs")


class File(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=150, blank=True, null=True)
    file = models.FileField(
        storage=storage.FILE_STORAGE,
        max_length=300,
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.display_name

    def get_file(self):
        if self.file:
            return self.file.url
        return None

    def get_safe_url(self):
        url = self.file.url
        if USE_GCS and "/download/storage/v1/b/" in url:
            url = url.replace(
                "dev/file/https%3A/storage.googleapis.com/download/storage/v1/b/bridgtl-prt-d-bkt-apps/o/", "")
            url = url.replace("%252F", "%2F")
            url = url.replace("https%3A/", "https://")
            url = url.replace("%3F", "?")
            url = url.replace("%3D", "=")
            url = url.replace("%26", "&")
            url = url.split("?X-Goog-Algorithm")
            url = url[0]

        elif USE_RACKSPACE:
            rackspace_url = RACKSPACE_BASE_URL + '/'
            if 'http' in url:
                url = url.replace(rackspace_url, '')
            if not 'http' in url:
                url = rackspace_url + url

        return url

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
