'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: views.py
# Project: django-panel-core
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
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView 
from django.contrib.auth import login, logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from panel.libs.form import *
from panel.libs.view import ProtectedMixin
from panel.structures.authentication.models import EmailVerification

# Create your views here.
class LoginView(TemplateView):
    template_name = "login.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("authentication:login-success")

        return self.render_to_response({
            "form" : AuthForm(request)
        })

    def post(self, request):
        next = request.GET.get("next")
        form = AuthForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())

            if next:
                return redirect(next)
            else:
                return redirect("authentication:login-success")
        else:
            return self.render_to_response({"form":form})

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
            messages.success(request, 'Your password has been changed.')
            return redirect("authentication:change-password-success")
        else:
            return self.render_to_response({"form":form})

class ChangePasswordSuccessView(TemplateView):
    template_name = "change-password-success.html"
    
    def get(self, request):
        return self.render_to_response({})

class EmailVerifyView(TemplateView):
    template_name = "email_verify.html"
    
    def get(self, request):
        code = request.GET.get('c')
        ev = get_object_or_404(EmailVerification, code=code, is_verified=False)
        ev.is_verified = True
        ev.save()
        ev.user.is_active = True
        ev.user.save()
        form = SetPasswordForm(ev.user)
        return self.render_to_response({
            'word' : 'Dear %s, your email <%s> has been verified' % (ev.user.full_name, ev.email),
            'form' : form
        })

    def post(self, request):
        code = request.GET.get('c')
        ev = get_object_or_404(EmailVerification, code=code)
        form = SetPasswordForm(ev.user, request.POST)
        print(ev.user.email)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been set.')
            return redirect("authentication:login")
        else:
            messages.error(request, form.errors)
            return self.render_to_response({
                'is_failed_set_password' : True,
                'form' : form
            })
