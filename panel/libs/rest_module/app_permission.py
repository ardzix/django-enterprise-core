# REST Module
from rest_framework import permissions

# Core WECARE
from core.structures.device.models import Application, DeviceType


class AllowApps(permissions.BasePermission):
    """
    Allow Accessing API if there is ID and Secret in Header
    """

    def has_permission(self, request, view):
        application = devicetype = None

        app_id = request.META.get('HTTP_X_WECARE_APP_ID')
        secret = request.META.get('HTTP_X_WECARE_SECRET')
        device_type = request.META.get('HTTP_X_DEVICE_TYPE')

        if not app_id and not secret and not device_type:
            return False

        if device_type:
            try:
                devicetype = DeviceType.objects.get(
                    short_name=device_type.lower())
            except DeviceType.DoesNotExist:
                return False

        try:
            application = Application.objects.get(app_id=app_id, secret=secret,
                                                  is_active=True, device_type=devicetype)
        except Application.DoesNotExist:
            return False
        else:
            return True
