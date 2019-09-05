'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: urls.py
# Project: django-enterprise-core
# File Created: Wednesday, 22nd August 2018 12:42:51 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 22nd August 2018 12:42:51 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.conf.urls import url, include
from .views import IndexView
from .views.user import UserView, UserFormView
from .views.group import GroupView, GroupFormView
from .views.permission import PermissionView, PermissionFormView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    # User
    url(r'^user/$', UserView.as_view(), name='user'),
    url(r'^user/form/$', UserFormView.as_view(), name='user-form'),

    # Group
    url(r'^group/$', GroupView.as_view(), name='group'),
    url(r'^group/form/$', GroupFormView.as_view(), name='group-form'),

    # Permission
    url(r'^permission/$', PermissionView.as_view(), name='permission'),
    url(r'^permission/form/$',
        PermissionFormView.as_view(),
        name='permission-form'),
]
