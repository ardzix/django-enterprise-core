'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: tracker.py
# Project: <<projectname>>
# File Created: Tuesday, 19th February 2019 3:00:02 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Tuesday, 19th February 2019 3:00:02 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.conf import settings
from enterprise.libs.ip_address import get_client_ip


class TrackerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = None
        if not request.user.is_anonymous:
            user = request.user

        tracking_id = request.GET.get('tracking_id')
        if not tracking_id:
            tracking_id = request.GET.get('track_id')
        if not tracking_id:
            tracking_id = request.GET.get('t_id')

        referer = request.META.get('HTTP_REFERER')
        useragent = request.META.get('HTTP_USER_AGENT')
        ip_address = get_client_ip(request)
        visited_page = "%s%s" % (
            request.META.get('HTTP_HOST'),
            request.get_full_path()
        )

        Tracker = self.get_model()
        tracker = Tracker()

        tracker.created_by = user
        tracker.ip = ip_address
        tracker.useragent = useragent[0:128] if useragent else None
        tracker.referer = referer[0:128] if referer else None
        tracker.trigger_action = request.method
        tracker.tracking_id = tracking_id
        tracker.visited_page = visited_page.split('?')[0]
        tracker.save()

        request.fb_app_id = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY')

        return super().dispatch(request, *args, **kwargs)

    def get_model(self):
        from ...structures.tracker.models import Tracker
        return Tracker
