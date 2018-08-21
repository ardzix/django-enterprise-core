'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: views.py
# Project: django-panel-core
# File Created: Tuesday, 21st August 2018 11:35:18 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 21st August 2018 11:35:58 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("You're looking at question index")