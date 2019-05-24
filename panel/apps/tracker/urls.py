'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: urls.py
# Project: <<projectname>>
# File Created: Wednesday, 20th February 2019 2:54:10 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Wednesday, 20th February 2019 2:54:10 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.conf.urls import url, include
from .views import IndexView
from .views.raw import RawView

urlpatterns = [
    url(r'^raw/$', RawView.as_view(), name='raw'),
    url(r'^$', IndexView.as_view(), name='index'),
]
