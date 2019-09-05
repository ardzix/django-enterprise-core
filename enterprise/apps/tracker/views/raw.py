'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: raw.py
# Project: <<projectname>>
# File Created: Wednesday, 20th February 2019 3:07:06 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Wednesday, 20th February 2019 3:07:07 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView

from datatable import Datatable

from ....libs.view import ProtectedMixin
from ....structures.tracker.models import Tracker


class RawView(ProtectedMixin, TemplateView):
    template_name = "log/raw.html"
    model_class = Tracker

    def get(self, request):
        if request.GET.get('draw', None) is not None:
            return self.datatable(request)

        return self.render_to_response({
            'title': "Tracker enterprise - %s" % self.model_class.__name__,
        })

    def datatable(self, request):
        qs = self.model_class.objects.all()
        defer = ['created_at', 'created_by', 'visited_page', 'referer', 'ip']

        d = Datatable(request, qs, defer, key="id")
        d.set_lookup_defer(['created_by__stage_name'])

        return d.get_data()
