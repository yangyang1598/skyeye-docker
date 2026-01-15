from django.contrib import admin
from .models import *
from datetime import timedelta

# Register your models here.
class CameraViewAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'camera_view_id', 'site_id', 'format_date', 'latitude', 'longitude',
        'cardinal_direction')
    fields=['name', 'installation_date', 'helikite_serial_number', 'gcs_serial_number',
        'missiondevice_serial_number', 'winch_serial_number']
    def format_date(self, obj):
        obj.date = obj.date + timedelta(hours=9)
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')

    format_date.admin_order_field = 'date'
    format_date.short_description = 'Date'
# admin.site.register(Poi, PoiAdmin)
    
admin.site.register(CameraView, CameraViewAdmin)
