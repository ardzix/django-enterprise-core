from __future__ import unicode_literals

import uuid
import time
# Django Module
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import six, text
from django.utils.http import int_to_base36
from django.utils.crypto import salted_hmac
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver

from core.libs.storage import STORAGE_FINAL_CHUNK
from core.structures.authentication.models import LakonUser
from core.structures.common.models.base import BaseModelGeneric
from core.structures.account.models import Brand
from core.structures.device.models import DeviceType


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
    created_by = models.ForeignKey(LakonUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128)
    folder = models.CharField(max_length=256)
    file = models.FileField(storage=private_storage, blank=True, null=True)
    cloud_file = models.FileField(
        storage = STORAGE_FINAL_CHUNK,
        max_length=300,
        blank = True,
        null = True
    )
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.filename


class EmailVerification(BaseModelGeneric): 
    email = models.EmailField()
    code = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
            return self.email


class APIIntegration(BaseModelGeneric):
    API_CHOICES = (
        ('one', 'One Signal'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'Whatsapp'),
        ('twitter', 'Twitter'),
        ('google', 'Google'),
        ('instagram', 'Instagram'),
    )
    api = models.CharField(max_length=15, choices=API_CHOICES, default="one")
    uid = models.CharField(max_length=256, blank=True, null=True)
    access_token = models.CharField(max_length=256)

    def __str__(self,):
        return "{api} {username}".format(api=self.get_api_display(), 
                                username=self.owned_by.stage_name)



@receiver(pre_save, sender=EmailVerification)
def process_email_verification_score(sender, instance, **kwargs):
    from core.structures.score.handlers.account import EmailVerificationHandler

    if instance.is_verified:
        score = EmailVerificationHandler(instance)
        score.process()

@receiver(post_save, sender=EmailVerification)
def process_email_verification(sender, instance, created, **kwargs):
    if not created and instance.is_verified:
        user = instance.created_by
        user.email = instance.email
        user.save()

@receiver(post_save, sender=APIIntegration)
def generate_social_oauth_data(sender, instance, created, **kwargs):
    from social_django.models import UserSocialAuth

    usa, created = UserSocialAuth.objects.get_or_create(
        user = instance.created_by, 
        provider = instance.api, 
        uid = instance.uid
    )

    usa.extra_data['access_token'] = instance.access_token
    usa.save()


@receiver(post_delete, sender=ChunkedUpload)
def delete_chunkfile_at_rackspace(sender, instance, **kwargs):
    if STORAGE_FINAL_CHUNK.exists(str(instance.cloud_file)):
        STORAGE_FINAL_CHUNK.delete(str(instance.cloud_file))


class Application(BaseModelGeneric):
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE)
    app_id = models.UUIDField(default=uuid.uuid4)
    secret = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    device_type = models.ForeignKey(DeviceType, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ts_b36 = int_to_base36(int(time.time()))
        key_salt = settings.SECRET_KEY
        hash = salted_hmac(
            six.text_type(key_salt),
            six.text_type(self.created_by.password),
        ).hexdigest()[::2]
        self.short_name = text.slugify(self.display_name)
        self.secret = "%s-%s" % (ts_b36, hash)

        return super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"