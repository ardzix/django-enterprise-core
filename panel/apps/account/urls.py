'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: urls.py
# Project: django-panel-core
# File Created: Tuesday, 21st August 2018 11:36:17 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 21st August 2018 11:36:17 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
]