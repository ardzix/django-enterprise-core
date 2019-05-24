from django.contrib import admin
from .models import ResizeImageTemp


class ResizeAdmin(admin.ModelAdmin):
    model = ResizeImageTemp


admin.site.register(ResizeImageTemp, ResizeAdmin)
