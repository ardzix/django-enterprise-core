from __future__ import unicode_literals
import timeago
from datetime import timedelta
from itertools import chain
from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models as geo
from django.contrib.gis.geos import Point
from django.contrib.sites.models import Site
from django.db.models import Manager as GeoManager
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from enterprise.libs.moment import to_timestamp
from enterprise.libs.base62 import base62_encode


User = settings.AUTH_USER_MODEL


class _BaseAbstract(models.Model):
    site = models.ForeignKey(Site, related_name="%(app_label)s_%(class)s_site",
                             blank=True, null=True, on_delete=models.CASCADE,)
    nonce = models.CharField(max_length=128, blank=True, null=True)
    id62 = models.CharField(
        max_length=100,
        db_index=True,
        blank=True,
        null=True)

    created_at = models.DateTimeField(db_index=True)
    created_at_timestamp = models.PositiveIntegerField(db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created_by")

    owned_at = models.DateTimeField(db_index=True)
    owned_at_timestamp = models.PositiveIntegerField(db_index=True)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="%(app_label)s_%(class)s_owner")

    updated_at = models.DateTimeField(db_index=True, blank=True, null=True)
    updated_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    updated_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_updated_by")

    published_at = models.DateTimeField(blank=True, null=True)
    published_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    published_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name="%(app_label)s_%(class)s_published_by")

    unpublished_at = models.DateTimeField(blank=True, null=True)
    unpublished_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    unpublished_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name="%(app_label)s_%(class)s_unpublished_by")

    approved_at = models.DateTimeField(blank=True, null=True)
    approved_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    approved_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                    related_name="%(app_label)s_%(class)s_approved_by")

    unapproved_at = models.DateTimeField(blank=True, null=True)
    unapproved_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    unapproved_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name="%(app_label)s_%(class)s_unapproved_by")

    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_at_timestamp = models.PositiveIntegerField(
        db_index=True, blank=True, null=True)
    deleted_by = models.ForeignKey(User, db_index=True, blank=True,
                                   null=True, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_deleted_by")

    objects = GeoManager()

    def save(self, *args, **kwargs):
        now = timezone.now()

        # set Point
        [
            self.set_lat_lng(name, getattr(self, name))
            for name in self.get_all_field_names()
            if isinstance(self._meta.get_field(name), geo.PointField)
        ]

        # create first time record
        if self.created_at is None:
            self.site = Site.objects.get_current()
            self.created_at = now
            self.created_at_timestamp = to_timestamp(self.created_at)
            if self.created_by:
                self.owned_by = self.created_by
                self.owned_at = self.created_at
                self.owned_at_timestamp = self.created_at_timestamp

        # always update
        self.updated_at = now
        self.updated_at_timestamp = to_timestamp(self.updated_at)

        # save the first time record
        instance = super(_BaseAbstract, self).save(*args, **kwargs)

        # generate id62
        if self.id and not self.id62:
            self.id62 = base62_encode(self.id)
            kwargs['force_insert'] = False
            instance = super(_BaseAbstract, self).save(*args, **kwargs)

        return instance

    def approve(self, user=None, *args, **kwargs):
        if user:
            # mark when the record deleted
            self.unapproved_at = None
            self.unapproved_at_timestamp = None
            self.unapproved_by = None
            self.approved_at = timezone.now()
            self.approved_at_timestamp = to_timestamp(self.approved_at)
            self.approved_by = user

            # save it
            return super(_BaseAbstract, self).save(*args, **kwargs)

    def unapprove(self, user=None, *args, **kwargs):
        if user:
            # mark when the record reovered
            self.approved_at = None
            self.approved_at_timestamp = None
            self.approved_by = None
            self.unapproved_at = timezone.now()
            self.unapproved_at_timestamp = to_timestamp(self.unapproved_at)
            self.unapproved_by = user

            # save it
            return super(_BaseAbstract, self).save(*args, **kwargs)

    def reject(self, user=None, *args, **kwargs):
        self.unapprove(user, *args, **kwargs)

    def publish(self, user=None, *args, **kwargs):
        if user:
            # mark when the record deleted
            self.unpublished_at = None
            self.unpublished_at_timestamp = None
            self.unpublished_by = None
            self.published_at = timezone.now()
            self.published_at_timestamp = to_timestamp(self.published_at)
            self.published_by = user

            # save it
            return super(_BaseAbstract, self).save(*args, **kwargs)

    def unpublish(self, user=None, *args, **kwargs):
        if user:
            # mark when the record reovered
            self.published_at = None
            self.published_at_timestamp = None
            self.published_by = None
            self.unpublished_at = timezone.now()
            self.unpublished_at_timestamp = to_timestamp(self.unpublished_at)
            self.unpublished_by = user

            # save it
            return super(_BaseAbstract, self).save(*args, **kwargs)

    def delete(self, user=None, *args, **kwargs):
        if user:
            # mark when the record deleted
            self.deleted_by = user

        self.deleted_at = timezone.now()
        self.deleted_at_timestamp = to_timestamp(self.deleted_at)

        # save it if there's a deleter
        return super(_BaseAbstract, self).save(*args, **kwargs)

    def permanent_delete(self, *args, **kwargs):
        return super(_BaseAbstract, self).delete(*args, **kwargs)

    def undelete(self, user=None, *args, **kwargs):
        if user:
            # mark when the record undeleted
            self.deleted_at = None
            self.deleted_at_timestamp = None
            self.deleted_by = user

            # save it if there's a deleter
            return super(_BaseAbstract, self).save(*args, **kwargs)

    def log(self, user, message, *args, **kwargs):
        log = Log()
        log.content_type = self.get_content_type()
        log.object_id = self.id
        log.logged_by = user
        log.message = message
        log.save()

        if kwargs.get("mention"):
            log.mentions.add(kwargs.get("mention"))
        log.save()

        return log

    # Getter
    def get_owner(self):
        return self.owned_by

    def get_creator(self):
        return self.created_by_by

    def get_created_at(self):
        return {
            'utc': self.created_at,
            'timestamp': self.created_at_timestamp,
            'timeago': timeago.format(self.created_at.replace(tzinfo=None) + timedelta(hours=7))
        }

    def get_deleted_at(self):
        return {
            'utc': self.deleted_at,
            'timestamp': self.deleted_at_timestamp,
            'timeago': timeago.format(self.deleted_at.replace(tzinfo=None) + timedelta(hours=7))
        }

    def get_approved_at(self):
        return {
            'utc': self.approved_at,
            'timestamp': self.approved_at_timestamp,
            'timeago': timeago.format(self.approved_at.replace(tzinfo=None) + timedelta(hours=7))
        }

    def get_published_at(self):
        return {
            'utc': self.published_at,
            'timestamp': self.published_at_timestamp,
            'timeago': timeago.format(self.published_at.replace(tzinfo=None) + timedelta(hours=7))
        }

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_lat_lng(self, field_name):
        point = getattr(self, field_name, None)

        if point is not None and hasattr(point, "x") and hasattr(point, "y"):
            return {
                'latitude': point.y,
                'longitude': point.x
            }
        else:
            return {
                'latitude': 0,
                'longitude': 0
            }

    def get_all_sizes(self, field_name, sizes=None):
        if field_name in self._meta.get_all_field_names():
            image = getattr(self, field_name)

            if hasattr(image, "path"):
                return generate_all_sizes(image.path, sizes=sizes)

    def get_status(self):
        if not self.approved_by and self.unapproved_by:
            approve_message = "REJECTED"
        elif self.approved_by and not self.unapproved_by:
            approve_message = "APPROVED"
        else:
            approve_message = "waiting to be approved"

        if not self.published_by and self.unpublished_by:
            publish_message = "UNPUBLISHED"
        elif self.published_by and not self.unpublished_by:
            publish_message = "PUBLISHED"
        else:
            publish_message = "waiting to be published"

        return "Approval status: (%s), Publish status: (%s)" % (
            approve_message, publish_message)

    # Setter
    def set_lat_lng(self, field_name, value):
        point = None

        if hasattr(
                self, field_name) and value and "longitude" in value and "latitude" in value:
            point = Point(value["longitude"], value["latitude"])
            setattr(self, field_name, point)

        return point

    # Backward
    def get_all_field_names(self):
        return list(
            set(
                chain.from_iterable(
                    (field.name, field.attname) if hasattr(
                        field, 'attname') else (field.name,)
                    for field in self._meta.get_fields()
                    # For complete backwards compatibility, you may want to exclude
                    # GenericForeignKey from the results.
                    if not (field.many_to_one and field.related_model is None)
                )
            )
        )

    class Meta:
        abstract = True


class BaseModelGeneric(_BaseAbstract):
    created_by = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created_by")

    class Meta:
        abstract = True


class BaseModelUnique(_BaseAbstract):
    created_by = models.OneToOneField(User, db_index=True, on_delete=models.CASCADE,
                                      related_name="%(app_label)s_%(class)s_created_by")

    class Meta:
        abstract = True
