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

class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.error_class = ErrorDiv

        self.fields["new_password1"].widget.attrs = {
            "class": "form-control"
        }
        self.fields["new_password2"].widget.attrs = {
            "class": "form-control"
        }