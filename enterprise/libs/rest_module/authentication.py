import datetime
import pytz

from django.utils.timezone import utc
from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from .permissions import *

SAFE_METHODS = ['GET', ]
EXPIRED_TOKEN = getattr(settings, 'EXPIRED_TOKEN', '24h')


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