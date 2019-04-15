'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: form.py
# Project: django-panel-core
# File Created: Tuesday, 21st August 2018 11:56:49 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 21st August 2018 11:56:49 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.forms.utils import ErrorList
from django.contrib.auth.forms import *
from django import forms

from panel.structures.authentication.models import User, EmailVerification, send_verification_email

class ErrorDiv(ErrorList):
    def __str__(self):
        return self.as_divs()

    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        else:
            errors = ''.join(['<div class="error">%s</div>' % e for e in self])
            return '<div class="errors">%s</div>' % errors

class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }

        self.fields['username'].label = 'Email/Phone Number'

        self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            if self.user_cache is None:
                user_temp = User.objects.filter(email=username).first()
                if user_temp and user_temp.is_active:
                    ev = EmailVerification.objects.filter(email=username).first()
                    if ev and ev.is_verified:
                        self.user_cache = authenticate(
                            self.request, 
                            username=user_temp.phone_number, 
                            password=password
                        )
                        if self.user_cache is None:
                            raise self.get_invalid_login_error()
                        else:
                            self.confirm_login_allowed(self.user_cache)
                            return self.cleaned_data

                    else:
                        self.verify_email(username, user_temp)

                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


    def verify_email(self, email, user):
        try:
            ev = send_verification_email(email, user)
            ev.user = user
            ev.save()
        except Exception as e:
            raise forms.ValidationError(e)
        raise forms.ValidationError('Your email has not been verified, we sent you an email to verify it')

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields['old_password'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['new_password1'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['new_password2'].widget.attrs = {
            'class': 'form-control'
        }

class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields['new_password1'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['new_password2'].widget.attrs = {
            'class': 'form-control'
        }


class RegisterForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Full Name', 'class': 'form-control'}
    ))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number', 'class': 'form-control'}
    ))