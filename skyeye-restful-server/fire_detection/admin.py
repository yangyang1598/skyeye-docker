from django.apps import apps
from django.contrib import admin

from .models import Detection


class DetectionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'date', 'site_name', 'class_name')

    def site_name(self, obj):
        if obj.site_id is None:
            return '-'

        Site = apps.get_model('skyeye', 'Site')
        site = Site.objects.filter(site_id=obj.site_id).only('name').first()
        if not site or not site.name:
            return str(obj.site_id)
        return site.name

    site_name.short_description = 'site'


admin.site.register(Detection, DetectionAdmin)
