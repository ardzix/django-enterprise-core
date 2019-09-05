# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import APILog

# Create your views here.


def apilogger(meta_data):
    """
    Create log for api call each user
    """
    try:
        apilog = APILog.objects.create(**meta_data)
    except Exception as e:
        return False
    else:
        return True
