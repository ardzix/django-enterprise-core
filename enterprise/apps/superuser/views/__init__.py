'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: django-enterprise-core
# File Created: Wednesday, 22nd August 2018 12:45:04 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 22nd August 2018 12:45:05 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
from django.views.generic import TemplateView
from enterprise.libs.view import ProtectedMixin


class IndexView(ProtectedMixin, TemplateView):
    template_name = "superuser/index.html"

    def get(self, request):
        return self.render_to_response({})
