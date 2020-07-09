'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: form.py
# Project: core.lakon.app
# File Created: Friday, 7th September 2018 3:50:58 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Friday, 7th September 2018 3:51:22 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Lakon, lakon.app
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


import nexmo
import uuid
import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.contrib.auth.forms import *
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from .nonce import NonceObject

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

        self.fields["username"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["password"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["username"].label = "Phone number"

class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["new_password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password2"].widget.attrs = {
            "class": "form-control"
        }


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["old_password"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password2"].widget.attrs = {
            "class": "form-control"
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("phone_number",)


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["phone_number"].widget.attrs = {
            "class": "form-control"
        }

        self.fields["password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["password1"].required=False

        self.fields["password2"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["password2"].required=False


class PhoneCheckForm(forms.ModelForm):
    request_id = None
    phone_number = None

    class Meta:
        model = get_user_model()
        fields = ("phone_number",)

    def clean(self):
        cleaned_data = super().clean()
        phone = self.cleaned_data.get('phone_number')

        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        verify_resp = client.start_verification(number=phone, brand='lakon.app')
        if not verify_resp['status'] == '0' and not verify_resp['status'] == '10':
            raise forms.ValidationError(
                verify_resp['error_text']
            )

        self.request_id = verify_resp['request_id']
        self.phone_number = phone

        return cleaned_data


class PhoneVerifyForm(forms.Form):
    code = forms.IntegerField(
        label=_("Verification COde"),
        widget=forms.NumberInput,
        help_text="We are sending a code to your phone number, please write down here",
    )

    request_id = forms.CharField(
        widget=forms.HiddenInput
    )

    phone_number = forms.CharField(
        widget=forms.HiddenInput
    )

    def clean(self):
        cleaned_data = super().clean()
        code = self.cleaned_data.get('code')
        request_id = self.cleaned_data.get('request_id')
        client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
        response = client.check_verification(request_id, code=code)

        if not response['status'] == '0':
            raise forms.ValidationError(
                response['error_text']
            )

        return cleaned_data


class NonceModelForm(ModelForm):
    def save(self, created_by=None, commit=True):
        if not hasattr(self, 'cleaned_data'):
            raise ValidationError({'detail':'Please validate before saving'})

        if 'nonce' not in self.cleaned_data:
            if not self.instance.nonce:
                self.instance.nonce = str(uuid.uuid4())
        if created_by and getattr(self.instance, 'created_by', None) is None:
            self.instance.created_by = created_by

        return super(NonceModelForm, self).save(commit=commit)

    def get_class_name(self):
        return self.__class__.__name__

    def get_pretty_class_name(self):
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>", self.get_class_name())
