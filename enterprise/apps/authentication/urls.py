'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: urls.py
# Project: django-enterprise-core
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
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.conf.urls import url, include
from .views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # login
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/success/$', LoginSuccessView.as_view(), name='login-success'),

    # logout
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # change password
    url(r'^change-password/$',
        ChangePasswordView.as_view(),
        name='change-password'),
    url(r'^change-password/success/$',
        ChangePasswordSuccessView.as_view(),
        name='change-password-success'),

    url(r'^email_verify/$', EmailVerifyView.as_view(), name='email_verify'),
]
