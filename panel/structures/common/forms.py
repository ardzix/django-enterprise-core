'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: forms.py
# Project: <<projectname>>
# File Created: Thursday, 21st June 2018 4:49:59 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Thursday, 21st June 2018 4:49:59 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
from django.forms import *
from models import *
from django.contrib.contenttypes.models import ContentType


class LogForm(ModelForm):
    note = CharField(
        max_length=255,
        required=False
    )
    content_id62 = CharField(
        max_length=10,
        required=False,
        widget=TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Log
        exclude = ("content_model", "content_object", "object_id")
        widgets = {
            'content_type': Select(attrs={'class': 'full-width', 'data-placeholder': 'Content Type', 'data-init-plugin': 'select2'}),
            'mentions': SelectMultiple(attrs={'class': 'full-width', 'data-init-plugin': 'select2'}),
            'logged_by': Select(attrs={'class': 'full-width', 'data-init-plugin': 'select2'}),
        }
        labels = {
            'object_id': "Object",
        }
