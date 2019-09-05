'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: permission.py
# Project: django-enterprise-core
# File Created: Wednesday, 22nd August 2018 1:48:22 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 22nd August 2018 1:48:22 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Permission
from enterprise.libs.view import ProtectedMixin
from datatable import Datatable
from ..forms import PermissionForm


class PermissionView(ProtectedMixin, TemplateView):
    template_name = "superuser/permission.html"

    def get(self, request, *args, **kwargs):
        if request.GET.get('draw', None) is not None:
            return self.datatable(request)

        return self.render_to_response({
            'title': "Tracker enterprise - %s" % Permission.__name__,
        })

    def delete(self, request):
        o_id = request.body.decode('utf-8').split("=")[1]
        qs = Permission.objects.filter(id__exact=o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Permission.objects.all()
        defer = ['id', 'name', 'codename', 'content_type']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class PermissionFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/permission.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")

        if edit:
            form = PermissionForm(instance=Permission.objects.get(id=edit))
        else:
            form = PermissionForm()

        return self.render_to_response({"form": form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = PermissionForm(
                request.POST,
                instance=Permission.objects.get(
                    id=edit))
        else:
            form = PermissionForm(request.POST)

        if form.is_valid():
            permission = form.save(commit=False)
            permission.save()
            messages.success(
                request, _(
                    'Permission (%s) has been saved.' %
                    permission.name))
            return redirect("superuser:permission")
        else:
            return self.render_to_response({"form": form})
