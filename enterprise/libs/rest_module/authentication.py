import datetime
import pytz

from django.utils.timezone import utc
from django.conf import settings

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication

SAFE_METHODS = ['GET', ]
EXPIRED_TOKEN = getattr(settings, 'EXPIRED_TOKEN', '24h')


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


class ExpiringTokenAuthentication(TokenAuthentication):
    def __init__(self):
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        expired_time = self.get_expired_token()

        self.expired = utc_now - expired_time

    def get_expired_token(self):
        time_notation = ['s', 'm', 'h', 'd']
        expired_token_value = EXPIRED_TOKEN[:-1]
        expired_token_notation = EXPIRED_TOKEN[-1]

        if expired_token_notation not in time_notation:
            raise Exception('EXPIRED_TOKEN not valid. Available s, m, h, d. Example 24h')
        
        if expired_token_notation == 'd':
            expired_time = datetime.timedelta(days=int(expired_token_value))
        elif expired_token_notation == 'h':
            expired_time = datetime.timedelta(hours=int(expired_token_value))
        elif expired_token_notation == 'm':
            expired_time = datetime.timedelta(minutes=int(expired_token_value))
        elif expired_token_notation == 's':
            expired_time = datetime.timedelta(seconds=int(expired_token_value))
        
        return expired_time

    def authenticate_credentials(self, key):
        expired_time = self.expired
        model = self.get_model()

        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.created < expired_time:
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)
