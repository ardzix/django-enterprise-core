'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: moment.py
# Project: django-enterprise-core
# File Created: Thursday, 16th August 2018 11:49:22 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Thursday, 16th August 2018 11:49:22 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from datetime import datetime, timedelta
from django.utils.dateformat import format


def to_timestamp(dt):
    return format(dt, 'U')


def get_today_epoch():
    now = datetime.utcnow()
    return now.replace(now.year, now.month, now.day, 0, 0, 0, 0)


def get_difference_epoch(epoch):
    diff = datetime.utcnow() - epoch
    return int(diff.total_seconds() * 1000000)


def get_next_monday(today):
    today = today.date()
    return today + timedelta(days=-today.weekday(), weeks=1)


def get_last_monday(today, ):
    today = today.date()
    return today - timedelta(days=today.weekday(), )
