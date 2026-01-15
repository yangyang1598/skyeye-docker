from django.contrib import admin
from django import forms
from .models import *
from mission_device.models import MissiondeviceDataLog
from datetime import timedelta, datetime
import logging

db_logger = logging.getLogger('db')

class SiteAdminForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # availability가 Null인 Missiondevice만 선택 가능하도록 필터링
        self.fields['missiondevice_serial_number'].queryset = Missiondevice.objects.filter(availability__isnull=True,camera_serial_number__isnull=False).order_by('serial_number')

# Register your models here.
class SiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    form = SiteAdminForm
    list_display = (
        'name','installation_date', 'missiondevice_serial_number', 'winch_serial_number',
        'missiondevice_altitude_low', 'missiondevice_pressure_offset', 'winch_pressure_offset')
    
    fields=('name', 'installation_date','missiondevice_serial_number', 'winch_serial_number',
        'missiondevice_altitude_low', 'missiondevice_pressure_offset', 'winch_pressure_offset')
    # 정렬 기준 추가
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user_site_mapping = {
            'ulju': ['길천', '특구(대운산)', '특구(웰컴센터)'],
            'namgu': ['울산남구'],
            'junggu': ['울산중구'],
        }
        if request.user.username in user_site_mapping:
            allowed_sites = user_site_mapping[request.user.username]
            queryset = queryset.filter(name__in=allowed_sites)
        # name으로 정렬
        queryset = queryset.order_by('name')
        print(queryset)
        return queryset

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # 새 객체가 생성될 때만 site_id를 설정합니다.
            last_site = Site.objects.all().order_by('site_id').last()
            if last_site:
                obj.site_id = last_site.site_id + 1
            else:
                obj.site_id = 1
        super().save_model(request, obj, form, change)

    def altitude(self, obj):
        try:
            # 최근 1분 내에 생성된 로그 중 가장 최신 로그를 가져옴
            latest_log = MissiondeviceDataLog.objects.filter(missiondevice_serial_number=obj.missiondevice_serial_number, date__gte=datetime.now() - timedelta(minutes=1)).latest('missiondevice_data_log_id')
            return latest_log.altitude
        except MissiondeviceDataLog.DoesNotExist:
            # 최근 1분 내의 로그가 없으면 None을 반환
            return None

class PoiAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('poi_id', 'site', 'latitude', 'longitude', 'altitude', 'zoom_level')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        user_site_mapping = {
            'ulju': ['길천', '특구(대운산)', '특구(웰컴센터)'],
            'namgu': ['울산남구'],
            'junggu': ['울산중구'],
        }
        if request.user.username in user_site_mapping:
            try:
                allowed_sites = user_site_mapping[request.user.username]
                queryset = queryset.filter(site__name__in=allowed_sites)
            except Site.DoesNotExist:
                queryset = queryset.none()
        
        return queryset


admin.site.register(Site, SiteAdmin)
admin.site.register(Poi, PoiAdmin)
