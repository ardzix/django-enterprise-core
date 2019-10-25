'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: form.py
# Project: django-panel-core
# File Created: Tuesday, 17th September 2019 6:31:54 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 17th September 2019 6:31:55 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Hand-crafted & Made with Love
# Copyright - 2018 Ardz Co, https://github.com/ardzix/django-panel-core
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

from django.views.generic import TemplateView 
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

class FormViewMixin(TemplateView):
    template_name = None
    model_class = None
    form_class = None

    def get(self, request):
        edit = request.GET.get("edit")
        instance = None
        if edit:
            instance = get_object_or_404(
                self.model_class, id62=edit)
            form = self.form_class(
                instance=instance,
            )
        else:
            form = self.form_class()

        return self.render_to_response({
            'title': self.model_class.__name__,
            'form': form,
            'form_title': self.model_class.__name__
        })

    def post(self, request):
        edit = request.GET.get("edit")
        instance = None
        if edit:
            instance = get_object_or_404(
                self.model_class, id62=edit)
            form = self.form_class(
                request.POST,
                request.FILES,
                instance=instance
            )
        else:
            form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            if not edit:
                obj.created_by = request.user
            else:
                obj.updated_by = request.user
            obj.save()
            form.save_m2m()
            messages.success(
                request,
                '%s has been saved.' %
                self.model_class.__name__)
            return redirect(request.META.get('HTTP_REFERER'))

        return self.render_to_response({
            'title': self.model_class.__name__,
            'form': form,
            'form_title': self.model_class.__name__
        })