'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: form.py
# Project: django-enterprise-core
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
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-enterprise-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from django.forms.utils import ErrorList
from django.contrib.auth.forms import *
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from crispy_forms import helper, layout, bootstrap

from enterprise.structures.authentication.models import User, EmailVerification, send_verification_email


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


class AuthForm(forms.Form):
    phone_number = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'placeholder': _('Email/Phone number')})
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')})
    )

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data['phone_number']
        password = cleaned_data['password']
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            if getattr(settings, 'AUTO_VERIFY_EMAIL'):
                user_temp = User.objects.filter(email=phone_number).first()
                if user_temp and user_temp.is_active:
                    ev = EmailVerification.objects.filter(
                        email=phone_number).first()
                    if ev:
                        if ev.is_verified:
                            user = authenticate(
                                phone_number=user_temp.phone_number, password=password)
                        else:
                            self.add_error(
                                'phone_number',
                                _('Your email has not been verified, please check your email to verify it'))
                            self.verify_email(phone_number, user_temp)
            else:
                user = authenticate(
                            email=phone_number, password=password)

        if user:
            if user.is_active:
                cleaned_data['user'] = user
            else:
                self.add_error('phone_number', _('Your account is not active'))
        else:
            self.add_error(
                'phone_number',
                _('Email/Phone and Password missmatch'))

        return cleaned_data

    def verify_email(self, email, user):
        ev = send_verification_email(email, user, is_reset_password=True)
        ev.user = user
        ev.save()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.layout = layout.Layout(
            bootstrap.PrependedText(
                'phone_number',
                '<i class="fas fa-user"></i>',
                wrapper_class='col-md-12 m-b-10'
            ),
            bootstrap.PrependedText(
                'password',
                '<i class="fas fa-lock"></i>',
                wrapper_class='col-md-12'
            ),
        )
        self.helper.render_unmentioned_fields = True
        self.helper.disable_csrf = True


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
