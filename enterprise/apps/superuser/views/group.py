'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: group.py
# Project: django-enterprise-core
# File Created: Wednesday, 22nd August 2018 12:45:28 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Wednesday, 22nd August 2018 12:45:28 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from enterprise.libs.view import ProtectedMixin
from datatable import Datatable
from ..forms import GroupForm


class GroupView(ProtectedMixin, TemplateView):
    template_name = "superuser/group.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) is not None:
            return self.datatable(request)

        return self.render_to_response({
            'title': "Tracker enterprise - %s" % Group.__name__,
        })

    def delete(self, request):
        o_id = request.body.decode('utf-8').split("=")[1]
        qs = Group.objects.filter(id__exact=o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        def get_permission_list(self):
            return " | ".join(self.permissions.values_list("name", flat=True))

        Group.add_to_class("get_permission_list", get_permission_list)
        qs = Group.objects.all()
        defer = ['id', 'name', 'get_permission_list']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class GroupFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/group.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")

        if edit:
            form = GroupForm(instance=Group.objects.get(id=edit))
        else:
            form = GroupForm()

        return self.render_to_response({"form": form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = GroupForm(request.POST, instance=Group.objects.get(id=edit))
        else:
            form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.permissions.set(form.cleaned_data.get('permissions'))
            group.save()
            messages.success(
                request, _(
                    'Group (%s) has been saved.' %
                    group.name))
            return redirect("superuser:group")
        else:
            return self.render_to_response({"form": form})
