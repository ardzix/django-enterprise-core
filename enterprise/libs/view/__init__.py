'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: view.py
# Project: django-enterprise-core
# File Created: Tuesday, 21st August 2018 11:51:25 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Tuesday, 21st August 2018 11:51:25 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import locale
import base64
import arrow
import datetime
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from ..brand import BrandManager
User = settings.AUTH_USER_MODEL



class ProtectedMixin(LoginRequiredMixin):
    """
    Mixin that will perform user access checking
    """
    login_url = "/authentication/login/"
    name_space = None
    model = None
    is_index_page = False

    def dispatch(self, request, *args, **kwargs):

        # If user not logged in, redirect to login page
        if not request.user.is_authenticated:
            return redirect(reverse("authentication:login") +
                            "?next=" + request.path_info)

        # If user is not staff nor super, 403 will be given
        if not self.is_staff(request):
            return self.handle_no_permission(request, *args, **kwargs)

        # set app and model access for user to the request
        app_access = []
        model_access = []
        for ct_int in request.user.groups.distinct(
                'permissions__content_type__model').values_list('permissions__content_type', flat=True):
            ct = ContentType.objects.filter(id=ct_int).first()
            if ct:
                if ct.app_label not in app_access:
                    app_access.append(ct.app_label)
                model_access.append("%s:%s" % (ct.app_label, ct.model))

        # Then store the app_access and model_access to the request
        request.app_access = app_access
        request.model_access = model_access
        request.permission_codenames = request.user.groups.values_list(
            'permissions__codename', flat=True)
        if not self.name_space:
            self.name_space = request.resolver_match.namespace
        if not self.model:
            self.model = request.resolver_match.url_name.replace(
                "_", "").split("-")[0]

        if not self.app_allowed(request):
            return self.handle_no_permission(request, *args, **kwargs)

        if not self.permission_allowed(request):
            return self.handle_no_permission(request, *args, **kwargs)

        return super(ProtectedMixin, self).dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request, *args, **kwargs):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return permission_denied(
            request, "403: you're not authorized to access this app", template_name='home/403.html')

    def get_permissions(self, request, *args, **kwargs):
        return list(request.user.groups.distinct('permissions__codename').values_list(
            'permissions__codename', flat=True).all())

    def permission_allowed(self, request):
        if request.user.is_superuser:
            return True

        edit = request.GET.get("edit")
        if request.method == "GET":
            if "view_" + self.model in self.get_permissions(request):
                return True
            if self.is_index_page:
                return True
        elif edit and request.method == "POST":
            if "change_" + self.model in self.get_permissions(request):
                return True
        elif not edit and request.method == "POST":
            if "add_" + self.model in self.get_permissions(request):
                return True
        elif request.method == "DELETE":
            if "delete_" + self.model in self.get_permissions(request):
                return True
        elif edit and request.method == "PUT":
            if "approve_" + self.model in self.get_permissions(request):
                return True
            elif "publish_" + self.model in self.get_permissions(request):
                return True

        return False

    def app_allowed(self, request):
        if request.user.is_superuser:
            return True
        if self.name_space in request.app_access:
            return True
        if self.is_index_page:
            return True
        return False

    def is_staff(self, request):
        return (request.user.is_staff or request.user.is_superuser)


class BrandProtectedMixin(ProtectedMixin):
    brand = None

    def dispatch(self, request, *args, **kwargs):
        # If user not logged in, redirect to login page
        if not request.user.is_authenticated:
            return redirect(reverse("authentication:login") +
                            "?next=" + request.path_info)

        # If user not set the brand to interact with, redirect to set_brand
        # page
        if not request.session.get('brand'):
            return redirect(reverse("authentication:set_brand") +
                            "?next=" + request.path_info)

        brand_manager = BrandManager(user=request.user)
        brands = brand_manager.get_brands()

        if not brands:
            return self.handle_no_permission(request, *args, **kwargs)

        if not request.session.get(
                'brand') in brands.values_list('id62', flat=True):
            return self.handle_no_permission(request, *args, **kwargs)

        self.brand = brands.get(id62=request.session.get('brand'))
        request.brand = self.brand

        return super(BrandProtectedMixin, self).dispatch(
            request, *args, **kwargs)


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context

    def handle_no_permission(self, request, *args, **kwargs):
        return permission_denied(
            request, "403: you're not authorized to access this app")
