from django import forms
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import *
from skyeye.models import Site
import logging

db_logger = logging.getLogger('db')

class CameraAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'availability','remarks', 'maximum_angle_roll', 'minimum_angle_roll', 'maximum_angle_pitch', 'minimum_angle_pitch',
        'maximum_angle_yaw', 'minimum_angle_yaw', 'zoom_magnification', 'night_vision')

class MissiondeviceAdminForm(forms.ModelForm):
    class Meta:
        model = Missiondevice
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # availability가 Null인 Camera만 선택 가능하도록 필터링
        self.fields['camera_serial_number'].queryset = Camera.objects.filter(availability__isnull=True)
        
class MissiondeviceAdmin(admin.ModelAdmin):
    form = MissiondeviceAdminForm  # 커스텀 폼 사용
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'camera_serial_number', 'availability','remarks')

class MissiondeviceDataLogAdmin(admin.ModelAdmin):
    date_hierarchy = "date"
    list_filter =("date",)
    # 관리자 화면에 보여질 칼럼 지정
    list_per_page = 20
    list_display = (
        'date', 'latitude', 'longitude', 'roll', 'pitch', 'yaw', 'camera_roll',
        'camera_pitch', 'camera_yaw', 'camera_zoom', 'pressure', 'altitude', 'altitude2', 'altitude4', 'missiondevice_serial_number'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        one_week_ago = timezone.now() - timedelta(days=7)
        queryset = queryset.filter(date__gte=one_week_ago).select_related('missiondevice_serial_number')
        
        # 사용자별 접근 가능한 사이트 정의
        user_site_mapping = {
            'ulju': ['길천', '특구(대운산)', '특구(웰컴센터)'],
            'namgu': ['울산남구'],
            'junggu': ['울산중구'],
        }
        
        if request.user.username in user_site_mapping:
            try:
                from skyeye.models import Site
                allowed_sites = Site.objects.filter(name__in=user_site_mapping[request.user.username])
                allowed_devices = [site.missiondevice_serial_number for site in allowed_sites if site.missiondevice_serial_number]
                if allowed_devices:
                    queryset = queryset.filter(missiondevice_serial_number__in=allowed_devices)
                else:
                    queryset = queryset.none()
            except Exception:
                queryset = queryset.none()
        
        return queryset
    
admin.site.register(Missiondevice, MissiondeviceAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(MissiondeviceDataLog, MissiondeviceDataLogAdmin)
