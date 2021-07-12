from django.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as geo
from django.db.models import Manager as GeoManager
from django.conf import settings

from enterprise.libs.moment import to_timestamp
from enterprise.libs.ip_address import get_client_ip

User = settings.AUTH_USER_MODEL


class Tracker(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    created_at_timestamp = models.PositiveIntegerField(db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name="%(app_label)s_%(class)s_created_by")
    modified_at = models.DateTimeField(auto_now=True)
    point = geo.PointField(null=True,)
    useragent = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in seconds", default=-1)
    trigger_action = models.CharField(max_length=100)
    visited_page = models.URLField(blank=True, null=True)
    OS = models.CharField(max_length=128, blank=True, null=True)
    referer = models.CharField(max_length=128, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    objects = GeoManager()
    log = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.created_at = timezone.now()
        self.created_at_timestamp = to_timestamp(self.created_at)
        return super(Tracker, self).save(*args, **kwargs)

    def set_lat_lng(self, field_name, value):
        point = None

        if hasattr(
                self, field_name) and "longitude" in value and "latitude" in value:
            point = Point(value["longitude"], value["latitude"])
            setattr(self, field_name, point)
        return point

    class Meta:
        app_label = "tracker"


def create_tracker(request, trigger_action, is_get_or_create=False, log=None, os="web"):
    user = None
    if not request.user.is_anonymous:
        user = request.user

    useragent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)
    visited_page = request.META.get('HTTP_REFERER', None)

    tracker = None
    if is_get_or_create:
        tracker = Tracker.objects.filter(
            created_by=user,
            trigger_action=trigger_action,
            useragent=useragent)
        if not tracker.exists():
            tracker = Tracker()
        else:
            tracker = tracker.last()
    else:
        tracker = Tracker()

    tracker.created_by = user
    tracker.ip = ip_address
    tracker.useragent = useragent
    tracker.visited_page = visited_page
    tracker.trigger_action = trigger_action
    tracker.log = log
    tracker.OS = os
    tracker.save()
