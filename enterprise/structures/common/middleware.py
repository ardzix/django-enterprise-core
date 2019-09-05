from ...structures.common.views import apilogger


class APILogMiddleware(object):
    """
    Middleware for Log API every call
    will be add in settings.py MIDDLEWARE
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if (request.META.get("HTTP_HOST") == 'api.helloyuna.io' or
                request.META.get("HTTP_HOST") == '45.118.134.111:10001'):

            api_meta = {"user": None if request.user.is_anonymous else request.user,
                        "app_id": request.META.get('HTTP_X_YUNA_APP_ID'),
                        "uid": request.META.get('HTTP_X_YUNA_SECRET'),
                        "latitude": request.GET.get("lat"),
                        "longitude": request.GET.get("lng"),
                        "endpoint": request.META.get("PATH_INFO"),
                        "request_method": request.method
                        }

            apilogger(api_meta)

        return response


class PAYLogMiddleware(object):
    """
    Middleware for Log API every call
    will be add in settings.py MIDDLEWARE
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if (request.META.get("HTTP_HOST") == 'pay.helloyuna.io' or
                request.META.get("HTTP_HOST") == '45.118.134.111:8401'):

            api_meta = {"user": None if request.user.is_anonymous else request.user,
                        "app_id": request.META.get('HTTP_X_YUNA_APP_ID'),
                        "uid": request.META.get('HTTP_X_YUNA_SECRET'),
                        "latitude": request.GET.get("lat"),
                        "longitude": request.GET.get("lng"),
                        "endpoint": request.META.get("PATH_INFO"),
                        "request_method": request.method
                        }

            apilogger(api_meta)

        return response
