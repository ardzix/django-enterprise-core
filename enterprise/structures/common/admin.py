# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Log, APILog, File
# Register your models here.


class LogAdmin(admin.ModelAdmin):
    pass


class APILogAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Log, LogAdmin)
admin.site.register(APILog, APILogAdmin)
admin.site.register(File, FileAdmin)
