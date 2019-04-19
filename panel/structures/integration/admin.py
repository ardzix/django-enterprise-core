from django.contrib import admin
from .models import ChunkedUpload, APIIntegration


class UploadAdmin(admin.ModelAdmin):
	model = ChunkedUpload
	list_display = ['created_by', 'created_at', 'filename', 'is_done']

class IntegrationAdmin(admin.ModelAdmin):
	model = APIIntegration
	list_display = ('created_by', 'created_at', 'api', )
	list_filter = ('api',)
	list_search = ('created_by__stage_name')


admin.site.register(ChunkedUpload, UploadAdmin)
admin.site.register(APIIntegration, IntegrationAdmin)