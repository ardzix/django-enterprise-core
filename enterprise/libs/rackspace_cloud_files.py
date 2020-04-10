'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: rackspace_cloud_files.py
# Project: enterprise.ayopeduli.id
# File Created: Wednesday, 31st October 2018 11:12:48 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 31st October 2018 11:12:49 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Peduli sesama, sejahtera bersama
# Copyright - 2018 Ayopeduli.Id, ayopeduli.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import os
from rackspace import connection
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text as force_unicode, smart_str
from django.utils.functional import cached_property

from django.contrib.auth import get_user_model

"""
https://developer.openstack.org/sdks/python/openstacksdk/users/resource.html#openstack.resource.Resource
https://developer.openstack.org/sdks/python/openstacksdk/users/resources/object_store/v1/obj.html#openstack.object_store.v1.obj.Object
https://developer.openstack.org/sdks/python/openstacksdk/users/proxies/object_store.html
https://developer.openstack.org/sdks/python/openstacksdk/users/guides/object_store.html

conn.object_store
['bulk_delete', 'containers', 'copy_object', 'create_container', 'delete_account_metadata', 'delete_container', 'delete_container_metadata', 'delete_object', 'delete_object_metadata', 'download_object', 'get_account_metadata', 'get_container_metadata', 'get_object', 'get_object_metadata', 'objects', 'set_account_metadata', 'set_container_metadata', 'set_object_metadata', 'upload_object', 'wait_for_delete', 'wait_for_status']

conn
['alarm', 'authenticator', 'authorize', 'backup', 'bare_metal', 'block_store', 'cluster', 'compute', 'database', 'identity', 'image', 'key_manager', 'load_balancer', 'message', 'monitoring', 'network', 'object_store', 'orchestration', 'profile', 'session', 'telemetry', 'workflow']

container
['allow_create', 'allow_delete', 'allow_head', 'allow_list', 'allow_retrieve', 'allow_update',
'base_path', 'bytes', 'bytes_used',
'clear', 'content_type', 'convert_ids', 'count', 'create', 'create_by_id',
'delete', 'delete_by_id', 'delete_metadata',
'existing', 'find', 'from_id', 'from_name',
'get', 'get_by_id', 'get_data_by_id', 'get_headers', 'get_id', 'get_resource_name',
'head', 'head_by_id', 'head_data_by_id',
'id', 'id_attribute', 'if_none_match', 'is_content_type_detected', 'is_dirty', 'is_newest', 'items', 'iteritems', 'iterkeys', 'itervalues',
'keys',
'list', 'location',
'metadata',
'name', 'name_attribute',
'new',
'object_count', 'patch_update', 'pop', 'popitem',
'read_ACL', 'resource_key', 'resource_name', 'resources_key',
'service', 'set_headers', 'set_metadata', 'setdefault', 'sync_key', 'sync_to',
'timestamp', 'to_dict', 'update', 'update_attrs', 'update_by_id', 'values', 'versions_location', 'write_ACL']

obj
[
'accept_ranges', 'allow_create', 'allow_delete', 'allow_head', 'allow_list', 'allow_retrieve', 'allow_update',
'base_path', 'bytes', 'clear', 'container', 'content_disposition', 'content_encoding', 'content_length', 'content_type', 'convert_ids', 'copy_from', 'create', 'create_by_id', 'data', 'delete', 'delete_after', 'delete_at', 'delete_by_id', 'delete_metadata', 'etag', 'existing', 'expires_at', 'find', 'from_id', 'from_name', 'get', 'get_by_id', 'get_data_by_id', 'get_headers', 'get_id', 'get_resource_name', 'hash', 'head', 'head_by_id', 'head_data_by_id', 'id', 'id_attribute', 'if_match', 'if_modified_since', 'if_none_match', 'if_unmodified_since', 'is_content_type_detected', 'is_dirty', 'is_newest', 'is_static_large_object', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'last_modified_at', 'list', 'location', 'metadata', 'multipart_manifest', 'name', 'name_attribute', 'new', 'object_manifest', 'patch_update', 'pop', 'popitem', 'range', 'resource_key', 'resource_name', 'resources_key', 'service', 'set_headers', 'set_metadata', 'setdefault', 'signature', 'timestamp', 'to_dict', 'transfer_encoding', 'update', 'update_attrs', 'update_by_id', 'values']
"""
conn = connection.Connection(
    username=settings.RACKSPACE_CLOUD_FILES["username"],
    api_key=settings.RACKSPACE_CLOUD_FILES["key"],
    region=settings.RACKSPACE_CLOUD_FILES["region"]
)


@deconstructible
class RackspaceStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        if not settings.USE_RACKSPACE:
            return None

        default_container = kwargs.get(
            "container", settings.RACKSPACE_CLOUD_FILES["default_container"])
        self.purpose = kwargs.pop("purpose")
        self.container = conn.object_store.get_container_metadata(
            default_container)
        super(RackspaceStorage, self).__init__(*args, **kwargs)

    def _open(self, name, mode='rb'):
        # This must return a File object
        return ContentFile(conn.object_store.get_object(
            name, container=self.container))

    def _save(self, name, content, encode_name=True):
        # Should return the actual name of name of the file saved (usually the
        # name passed in, but if the storage needs to change the file name
        # return the new name instead).
        if encode_name:
            name = self.get_valid_name(name)

        uploaded = conn.object_store.upload_object(
            container=self.container,
            name=name,
            data=content
        )

        # resize here, send to celery
        if self.purpose and hasattr(uploaded, "name"):
            from enterprise.structures.integration.models import ResizeImageTemp
            rit = ResizeImageTemp(
                image=self.url(
                    uploaded.name),
                purpose=self.purpose)
            rit.created_by = get_user_model().objects.first()
            rit.save()

        return name

    @cached_property
    def location(self):
        return self._location

    @cached_property
    def base_url(self):
        if self._base_url is not None and not self._base_url.endswith('/'):
            self._base_url += '/'
        return self._base_url

    def get_valid_name(self, name):
        form = "%Y-%m-%d"
        extension = os.path.splitext(name)[1]
        date = os.path.normpath(
            force_unicode(
                timezone.now().strftime(
                    smart_str(form)
                )
            )
        )
        rand_name = '%s%s' % (get_random_string(), extension)
        return '%s%s/%s' % (self.location, date, rand_name)

    def delete(self, name):
        # delete object
        conn.object_store.delete_object(
            name,
            ignore_missing=settings.DEBUG,
            container=self.container
        )

    def exists(self, name):
        return self.size(name) > 0

    def size(self, name):
        try:
            obj = conn.object_store.get_object_metadata(
                name, container=self.container)
        except BaseException:
            return 0
        return obj.content_length

    def url(self, name):
        return "%s%s" % (self.base_url, name)
