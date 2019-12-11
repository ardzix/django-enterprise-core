'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: mixin.py
# Project: <<projectname>>
# File Created: Wednesday, 6th November 2019 2:17:25 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
# 
# Last Modified: Wednesday, 6th November 2019 2:17:25 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import jwt
from rest_framework.permissions import *
from django.conf import settings

class JWTAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not settings.VALIDATE_JWT:
            return True
        if not request.data.get('encoded'):
            raise exceptions.ParseError(detail='Please wrap your data with JWT in \'encoded\' ')
        try:
            decoded = jwt.decode(request.data.get('encoded'), settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHMS)
        except Exception as e:
            raise exceptions.AuthenticationFailed(detail=str(e))
        request._full_data = decoded
        # decoded = jwt.decode(encoded, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHMS)
        return True