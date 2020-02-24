'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: viewset.py
# Project: core.lakon.app
# File Created: Wednesday, 5th September 2018 1:23:29 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 5th September 2018 1:23:29 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

from rest_framework import mixins
from enterprise.libs.rest_module.permission import JWTAuthenticated, IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from .authentication import *


class PublicGenericViewSet(GenericViewSet):
    """
    Every authenticated user have access to the contents,
    but only owner has permission to update/delete
    """
    lookup_field = 'id62'

    def initialize_request(self, request, *args, **kwargs):
        su = super().initialize_request(
            request,
            *
            args,
            **kwargs)
        self.set_permissions()
        return su

    def set_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'delete']:
            permission_classes = [IsOwnerAuthenticated]
        elif self.action in ['post']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        self.permission_classes = permission_classes
        return [permission() for permission in permission_classes]


class UGCGenericViewSet(GenericViewSet):
    """
    Every authenticated user have access to the contents,
    but only owner has permission to update/delete
    """
    lookup_field = 'id62'

    def initialize_request(self, request, *args, **kwargs):
        su = super().initialize_request(
            request,
            *
            args,
            **kwargs)
        self.set_permissions()
        return su

    def set_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'delete']:
            permission_classes = [IsOwnerAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        self.permission_classes = permission_classes
        return [permission() for permission in permission_classes]


class PrivateContentGenericViewSet(GenericViewSet):
    """
    Only object owner have access to the contents
    """
    lookup_field = 'id62'

    def initialize_request(self, request, *args, **kwargs):
        su = super().initialize_request(request,*args,**kwargs)
        self.set_permissions()
        return su

    def set_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['retrieve', 'update', 'delete']:
            permission_classes = [IsOwnerAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        self.permission_classes = permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request):
        self.queryset = self.queryset.filter(
            owned_by=request.user
        ).order_by('-created_at')
        return super().list(request)


class JWTGenericViewSet(GenericViewSet):
    """
    View protected bt JWT
    """
    lookup_field = 'id62'

    def initialize_request(self, request, *args, **kwargs):
        su = super().initialize_request(request,*args,**kwargs)
        self.permission_classes = [JWTAuthenticated]
        return su


class UGCViewSet(UGCGenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin):
    pass


class PrivateContentViewSet(PrivateContentGenericViewSet,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin):
    pass


class PrivateContentRetrieveViewSet(PrivateContentGenericViewSet,
                                    mixins.RetrieveModelMixin,
                                    mixins.ListModelMixin):
    pass


class RetrieveViewSet(UGCGenericViewSet,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin):
    pass


class SingleObjectOwnedViewSet(UGCGenericViewSet,
                               mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin):
    pass
