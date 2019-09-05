from django.contrib import admin
from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'created_by', 'ip', 'trigger_action')


admin.site.register(Tracker, TrackerAdmin)
