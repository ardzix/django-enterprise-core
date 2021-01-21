import jwt

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, BasePermission

from django.conf import settings


SAFE_METHODS = ['GET', ]


class IsOwnerAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        is_authenticated = super(
            IsOwnerAuthenticated,
            self).has_permission(
            request,
            view)
        return is_authenticated and view.get_object().owned_by == request.user


class IsCreatorAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        is_authenticated = super(
            IsCreatorAuthenticated,
            self).has_permission(
            request,
            view)
        return is_authenticated and view.get_object().created_by == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        elif view.action in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if view.action in ['list', 'retrieve']:
            return True

        # if not list or retrieve, if not log in then always False
        if not request.user.is_authenticated:
            return False
        return obj.owned_by == request.user


class IsReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):

        return (
            request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        if view.action in ['list', 'retrieve']:
            return True

        # if not list or retrieve, if not log in then always False
        return False


class PanelPermission(BasePermission):
    """
    The request is authenticated as a staff with certain persmissions, or superuser.
    """
    ACTION_DICT = {
        'list': 'view',
        'retrieve': 'view',
        'create': 'add',
        'update': 'change',
        'partial_update': 'change',
        'destroy': 'delete'
    }

    def has_permission(self, request, view):
        # If user is super, return True
        if request.user.is_authenticated and request.user.is_superuser or request.user.is_staff:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Allow if user is superuser
        if request.user.is_superuser:
            return True

        # get user permissions
        permission_codenames = list(request.user.groups.values_list(
            'permissions__codename', flat=True))
        permission_codenames += list(request.user.user_permissions.values_list(
            'codename', flat=True))

        # specify this view action
        model_name = ContentType.objects.get_for_model(obj).model
        action_name = '%s_%s' % (self.ACTION_DICT[view.action], model_name)

        # check if this view action in user permissions
        if action_name in permission_codenames:
            return True
        return False

class JWTAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not settings.VALIDATE_JWT:
            return True
        if not request.data.get('encoded'):
            raise exceptions.ParseError(
                detail='Please wrap your data with JWT in \'encoded\' ')
        try:
            decoded = jwt.decode(request.data.get(
                'encoded'), settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHMS)
        except Exception as e:
            raise exceptions.AuthenticationFailed(detail=str(e))
        request._full_data = decoded
        # decoded = jwt.decode(encoded, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHMS)
        return True
