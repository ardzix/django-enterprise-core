from __future__ import unicode_literals
from core.libs.moment import to_timestamp
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from core.structures.authentication.models import LakonUser as User
import json

# Create your models here.
class Log(models.Model):
    content_type = models.ForeignKey(ContentType, 
                    related_name="%(app_label)s_%(class)s_content_type", 
                    blank=True, null=True, on_delete=models.CASCADE,)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    logged_at = models.DateTimeField(blank=True, null=True)
    logged_at_timestamp = models.PositiveIntegerField(blank=True, null=True)
    logged_by = models.ForeignKey(User, db_index=True,  on_delete=models.CASCADE,)
    
    def __unicode__(self):
        return self.logged_by.username

    def get_message_dict(self):
        try:
            return json.loads(self.message)
        except:
            return {}

    def get_note(self):
        message_dict = self.get_message_dict()
        if "note" in message_dict:
            return message_dict['note']
        else:
            return "-"

    def get_mentions(self):
        return ', '.join(self.mentions.values_list("username", flat=True))

    def save(self, *args, **kwargs):
        self.logged_at = timezone.now()
        self.logged_at_timestamp = to_timestamp(self.logged_at)

        return super(Log, self).save(*args, **kwargs)

    def read(self, *args, **kwargs):
        self.read_at = timezone.now()
        self.read_at_timestamp = to_timestamp(self.read_at)

        return self.save(*args, **kwargs)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"


class APILog(models.Model):
    """
    For API log each call, each user
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True,  on_delete=models.CASCADE)

    app_id = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    endpoint = models.CharField(max_length=100)
    request_method = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __unicode__(self):
        return self.app_id

    class Meta:
        verbose_name = "APILog"
        verbose_name_plural = "APILogs"