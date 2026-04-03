from django.contrib import admin
from .models import *
from datetime import timedelta

# Register your models here.

class CameraAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'availability','remarks', 'maximum_angle_roll', 'minimum_angle_roll', 'maximum_angle_pitch', 'minimum_angle_pitch',
        'maximum_angle_yaw', 'minimum_angle_yaw', 'zoom_magnification', 'night_vision')

class CameraViewAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'camera_view_id', 'site_id', 'format_date', 'latitude', 'longitude',
        'cardinal_direction')
    def format_date(self, obj):
        obj.date = obj.date + timedelta(hours=9)
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')

    format_date.admin_order_field = 'date'
    format_date.short_description = 'Date'
    
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraView, CameraViewAdmin)
