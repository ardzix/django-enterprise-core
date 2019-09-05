'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: views.py
# Project: django-enterprise-core
# File Created: Tuesday, 21st August 2018 11:35:18 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Tuesday, 21st August 2018 11:35:58 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django import forms

from enterprise.libs.form import *
from enterprise.libs.view import ProtectedMixin
from enterprise.structures.authentication.models import EmailVerification


# Create your views here.
class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("authentication:login-success")

        return self.render_to_response({
            "form": AuthForm()
        })

    def post(self, request):
        next = request.GET.get("next")
        form = AuthForm(request.POST)

        if form.is_valid():
            login(request, form.cleaned_data['user'])
            if next:
                return redirect(next)
            else:
                return redirect("authentication:login-success")
        else:
            print(form.errors)
            return self.render_to_response({"form": form})


class LoginSuccessView(TemplateView):
    template_name = "login-success.html"

    def get(self, request):
        return self.render_to_response({})


class LogoutView(TemplateView):
    template_name = "logout.html"

    def get(self, request):
        logout(request)
        return self.render_to_response({})


class ChangePasswordView(ProtectedMixin, TemplateView):
    template_name = "change-password.html"

    def get(self, request):
        return self.render_to_response({
            "form": ChangePasswordForm(request.user)
        })

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _('Your password has been changed.'))
            return redirect("authentication:change-password-success")
        else:
            return self.render_to_response({"form": form})


class ChangePasswordSuccessView(TemplateView):
    template_name = "change-password-success.html"

    def get(self, request):
        return self.render_to_response({})


class ResetPasswordView(TemplateView):

    template_name = 'reset-password.html'

    def get(self, request):
        reset_form = SetPasswordForm()
        return self.render_to_response({
            'reset_form': reset_form,
            'base_url': settings.BASE_URL,
        })

    def post(self, request):
        reset_form = SetPasswordForm(request.POST)
        if reset_form.is_valid():
            messages.success(
                request,
                _('Your reset password request has been processed, please check your email'))
        else:
            messages.error(request, form.errors)

        return self.render_to_response({
            'reset_form': reset_form,
            'base_url': settings.BASE_URL,
        })


class EmailVerifyView(TemplateView):
    template_name = "email_verify.html"

    def get(self, request):
        code = request.GET.get('c')
        # ev = get_object_or_404(EmailVerification, code=code, is_verified=False)
        ev = get_object_or_404(EmailVerification, code=code)
        user = get_object_or_404(User, id=ev.user_id)

        ev.is_verified = True
        ev.save()
        user.is_active = True
        user.save()

        set_password_form = SetPasswordForm(user) \
            if request.GET.get('is_reset_password') \
            else None

        register_form = RegisterForm() \
            if request.GET.get('is_acquire_account') \
            else None

        return self.render_to_response({
            'word': _('Dear %s, your email <%s> has been verified' % (user.full_name, ev.email)),
            'set_password_form': set_password_form,
            'register_form': register_form,
        })

    def post(self, request):
        code = request.GET.get('c')
        ev = get_object_or_404(EmailVerification, code=code)

        set_password_form = SetPasswordForm(ev.user, request.POST) \
            if request.GET.get('is_reset_password') \
            else None

        register_form = RegisterForm(request.POST) \
            if request.GET.get('is_acquire_account') \
            else None

        if set_password_form:
            if set_password_form.is_valid():
                set_password_form.save()
                messages.success(request, _('Your password has been set.'))
                return redirect("authentication:login")
            else:
                messages.error(request, set_password_form.errors)

        if register_form:
            if register_form.is_valid():
                ev.user.full_name = register_form.cleaned_data['full_name']
                ev.user.nick_name = ev.user.full_name
                ev.user.phone_number = register_form.cleaned_data['phone_number']

                try:
                    ev.user.save()
                    messages.success(
                        request, _('You\'re successfully registered.'))
                    return redirect("authentication:login")
                except IntegrityError as e:
                    messages.error(request, str(e).split(':')[-1])
            else:
                messages.error(request, register_form.errors)

        return self.render_to_response({
            'is_failed_set_password': True,
            'is_failed_register': True,
            'set_password_form': set_password_form,
            'register_form': register_form,
        })
