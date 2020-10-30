import os
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text as force_unicode, smart_str
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from google.cloud import storage


class GoogleCloudStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        if not settings.USE_GCS:
            return None

        self.purpose = kwargs.pop('purpose')
        # connect to the bucket(kur-bri-co-id)
        self.client = storage.Client.from_service_account_json(
            settings.GCP_CREDENTIAL)

        super(GoogleCloudStorage, self).__init__(*args, **kwargs)

    def _open(self, name, mode='rb'):
        return ContentFile(self.get_blob(name).download_as_string())

    def _save(self, name, content, encode_name=True):
        if encode_name:
            # name will be something like 'dev/file/2020-10-13/kNnauKls.png'
            name = self.get_valid_name(name)

        # upload
        bucket = self.get_bucket()
        bucket = bucket.blob(name)

        # this upload file will return nothing
        bucket.upload_from_file(content)

        # get url
        uploaded = self.get_blob(name)

        if self.purpose and hasattr(uploaded, "name"):
            from enterprise.structures.integration.models import ResizeImageTemp
            rit = ResizeImageTemp(
                image=uploaded._properties['selfLink'],
                purpose=self.purpose)
            rit.created_by = get_user_model().objects.first()
            rit.save()

        return name

    def get_valid_name(self, name):
        extension = os.path.splitext(name)[1]
        date = os.path.normpath(
            force_unicode(
                timezone.now().strftime(
                    smart_str("%Y-%m-%d")
                )
            )
        )
        rand_name = f'{get_random_string()}{extension}'
        return f'testing/file/{date}/{rand_name}'

    @cached_property
    def location(self):
        return self._location

    @cached_property
    def base_url(self):
        if self._base_url:
            self._base_url = self._base_url
        return self._base_url

    def get_bucket(self, bucket_name=''):
        return self.client.bucket(bucket_name if bucket_name != '' else settings.GCS_BUCKET_NAME)

    def list_buckets(self):
        # Make an authenticated API request
        return self.client.list_buckets()

    def get_blob(self, name, bucket_name=''):
        """
        {
            'name': 'testing/2020-10-13/aMDGZDSoFTeP.png',
            '_properties': {'kind': 'storage#object',
            'id': 'kur-bri-co-id/testing/2020-10-13/aMDGZDSoFTeP.png/1602582777849390',
            'selfLink': 'https://www.googleapis.com/storage/v1/b/kur-bri-co-id/o/testing%2F2020-10-13%2FaMDGZDSoFTeP.png',
            'mediaLink': 'https://storage.googleapis.com/download/storage/v1/b/kur-bri-co-id/o/testing%2F2020-10-13%2FaMDGZDSoFTeP.png?generation=1602582777849390&alt=media',
            'name': 'testing/2020-10-13/aMDGZDSoFTeP.png',
            'bucket': 'kur-bri-co-id',
            'generation': '1602582777849390',
            'metageneration': '1',
            'contentType': 'image/png',
            'storageClass': 'STANDARD',
            'size': '3894',
            'md5Hash': '',
            'crc32c': '',
            'etag': '',
            'timeCreated': '2020-10-13T09:52:57.849Z',
            'updated': '2020-10-13T09:52:57.849Z',
            'timeStorageClassUpdated': '2020-10-13T09:52:57.849Z'},
            '_changes': set(),
            '_chunk_size': None,
            '_bucket': <Bucket: kur-bri-co-id>,
            '_acl': <google.cloud.storage.acl.ObjectACL at 0x11ffcb2e8>,
            '_encryption_key': None
        }
        """
        return self.get_bucket(bucket_name).get_blob(name)

    def list_blobs(self, bucket_name='', prefix=None, delimiter=None):
        """Lists all the blobs in the bucket that begin with the prefix.

        This can be used to list all blobs in a "folder", e.g. "public/".

        The delimiter argument can be used to restrict the results to only the
        "files" in the given "folder". Without the delimiter, the entire tree under
        the prefix is returned. For example, given these blobs:

            a/1.txt
            a/b/2.txt

        If you just specify prefix = 'a', you'll get back:

            a/1.txt
            a/b/2.txt

        However, if you specify prefix='a' and delimiter='/', you'll get back:

            a/1.txt

        Additionally, the same request will return blobs.prefixes populated with:

            a/b/
        """
        return self.get_bucket(bucket_name).list_blobs(
            prefix=prefix, delimiter=delimiter
        )

    def rename_blob(self, blob_name, new_name):
        blob = self.get_bucket().blob(blob_name)

        new_blob = self.get_bucket().rename_blob(blob, new_name)

        return
