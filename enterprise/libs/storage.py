'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: storage.py
# Project: core.ayopeduli.id
# File Created: Wednesday, 31st October 2018 7:26:00 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 31st October 2018 7:26:01 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.conf import settings
from django.core.files.storage import FileSystemStorage
from enterprise.libs.google_cloud_file import GoogleCloudStorage


USE_GCS = getattr(settings, 'USE_GCS', False)
USE_RACKSPACE = getattr(settings, 'USE_RACKSPACE', False)
GCS_BASE_URL = getattr(settings, 'GCS_BASE_URL', '')
RACKSPACE_BASE_URL = getattr(settings, 'RACKSPACE_BASE_URL', '')

def generate_name(instance, filename):
    pass


if settings.PRODUCTION:
    ROOT_URL = ""
    MEDIA_ROOT = "/var/www/html/upload/"
    UPLOAD_ROOT = "%supload/" % settings.BASE_URL
else:
    ROOT_URL = "dev/"
    MEDIA_ROOT = settings.MEDIA_ROOT
    UPLOAD_ROOT = "%sstatic/upload/" % settings.BASE_URL


if USE_RACKSPACE:
    from enterprise.libs.rackspace_cloud_files import RackspaceStorage

    BASE_URL = RACKSPACE_BASE_URL
    VIDEO_STORAGE = RackspaceStorage(
        location="%svideo/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="VIDEO_SIZES"
    )

    FILE_STORAGE = RackspaceStorage(
        location="%sfile/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="FILE"
    )

    AVATAR_STORAGE = RackspaceStorage(
        location="%spicture/avatar/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="AVATAR_PHOTO_SIZES"
    )

    COVER_STORAGE = RackspaceStorage(
        location="%spicture/cover/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="COVER_PHOTO_SIZES"
    )

    LOGO_STORAGE = RackspaceStorage(
        location="%spicture/logo/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="LOGO_PHOTO_SIZES"
    )

    PICTURE_STORAGE = RackspaceStorage(
        location="%spicture/others/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="PICTURE_PHOTO_SIZES"
    )

elif USE_GCS:
    BASE_URL = GCS_BASE_URL
    VIDEO_STORAGE = GoogleCloudStorage(
        location="%svideo/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="VIDEO_SIZES"
    )

    FILE_STORAGE = GoogleCloudStorage(
        location="%sfile/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="FILE"
    )

    AVATAR_STORAGE = GoogleCloudStorage(
        location="%spicture/avatar/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="AVATAR_PHOTO_SIZES"
    )

    COVER_STORAGE = GoogleCloudStorage(
        location="%spicture/cover/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="COVER_PHOTO_SIZES"
    )

    LOGO_STORAGE = GoogleCloudStorage(
        location="%spicture/logo/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="LOGO_PHOTO_SIZES"
    )

    PICTURE_STORAGE = GoogleCloudStorage(
        location="%spicture/others/" % ROOT_URL,
        base_url=BASE_URL,
        purpose="PICTURE_PHOTO_SIZES"
    )

else:
    VIDEO_STORAGE = FileSystemStorage(
        location='%s/video' %
        MEDIA_ROOT,
        base_url='%svideo/' %
        UPLOAD_ROOT)
    FILE_STORAGE = FileSystemStorage(
        location='%s/file' %
        MEDIA_ROOT,
        base_url='%sfile/' %
        UPLOAD_ROOT)
    AVATAR_STORAGE = FileSystemStorage(
        location='%s/picture/avatar' %
        MEDIA_ROOT,
        base_url='%spicture/avatar/' %
        UPLOAD_ROOT)
    COVER_STORAGE = FileSystemStorage(
        location='%s/picture/cover' %
        MEDIA_ROOT,
        base_url='%spicture/cover/' %
        UPLOAD_ROOT)
    LOGO_STORAGE = FileSystemStorage(
        location='%s/picture/logo' %
        MEDIA_ROOT,
        base_url='%spicture/logo/' %
        UPLOAD_ROOT)
    PICTURE_STORAGE = FileSystemStorage(
        location='%s/picture/others' %
        MEDIA_ROOT,
        base_url='%spicture/others/' %
        UPLOAD_ROOT)


# chunk upload storage
STORAGE_CHUNK = FileSystemStorage(
    location=settings.MEDIA_ROOT + "/chunk",
    base_url="%sstatic/upload/chunk/" % settings.BASE_URL,
)
