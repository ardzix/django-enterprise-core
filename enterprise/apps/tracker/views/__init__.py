'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: <<projectname>>
# File Created: Wednesday, 20th February 2019 3:00:43 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Wednesday, 20th February 2019 3:00:43 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView
from enterprise.libs.view import ProtectedMixin


class IndexView(ProtectedMixin, TemplateView):
    template_name = "log/index.html"

    def get(self, request):
        return self.render_to_response({})
