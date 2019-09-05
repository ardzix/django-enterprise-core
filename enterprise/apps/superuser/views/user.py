'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: user.py
# Project: <<projectname>>
# File Created: Monday, 10th December 2018 2:39:06 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         http://ardz.xyz>
#
# Last Modified: Monday, 10th December 2018 2:39:06 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Crafted by Pro
# Copyright - <<year>> Ardz & Co, -
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import get_user_model
from enterprise.libs.view import ProtectedMixin
from datatable import Datatable
from ..forms import UserForm


class UserView(ProtectedMixin, TemplateView):
    template_name = "superuser/user.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) is not None:
            return self.datatable(request)

        return self.render_to_response({
            'title': "Tracker enterprise - %s" % get_user_model().__name__,
        })

    def delete(self, request):
        o_id = request.body.decode('utf-8').split("=")[1]
        User = get_user_model()
        qs = User.objects.filter(id__exact=o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        User = get_user_model()
        qs = User.objects.all()
        defer = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'is_active',
            'is_staff',
            'is_superuser']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class UserFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/user.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")
        User = get_user_model()

        if edit:
            form = UserForm(
                instance=User.objects.get(
                    id=edit), initial={
                    'password': ''})
        else:
            form = UserForm()

        return self.render_to_response({"form": form})

    def post(self, request):
        edit = request.GET.get("edit")
        User = get_user_model()

        if edit:
            u = User.objects.get(id=edit)
            u_pass = u.password
            form = UserForm(request.POST, instance=u, initial={'password': ''})
        else:
            form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.groups.set(form.cleaned_data.get('groups'))

            if form.cleaned_data.get(
                    'password') and form.cleaned_data.get('password') != '':
                user.set_password(form.cleaned_data.get('password'))
            else:
                user.password = u_pass

            user.save()
            if hasattr(user, 'permissions'):
                user.permissions.set(form.cleaned_data.get('permissions'))
                user.save()
            messages.success(
                request, _(
                    'User (%s) has been saved.' %
                    user.full_name))
            return redirect("superuser:user")
        else:
            return self.render_to_response({"form": form})
