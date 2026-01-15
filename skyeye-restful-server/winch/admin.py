from django.contrib import admin
from .models import *
from skyeye.models import Site

# Register your models here.
class WinchAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'primary_sensor', 'extended_sensor', 'tetherline_length', 'tetherline_limit_tension',
        'production_year')

class WinchDataLogAdmin(admin.ModelAdmin):
    # date_hierarchy = "date"

    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'date', 'tetherline_angle', 'pressure', 'temperature','winch_serial_number')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # 사용자별 사이트 매핑 정의 (WinchAdmin과 동일)
        user_site_mapping = {
            'ulju': ['길천', '특구(대운산)', '특구(웰컴센터)'],
            'namgu': ['울산남구'],
            'junggu': ['울산중구'],
        }
        
        # 현재 사용자의 사이트 목록 가져오기
        user_sites = user_site_mapping.get(request.user.username)
        
        if user_sites:
            try:
                # 사용자에게 할당된 사이트들 찾기
                sites = Site.objects.filter(name__in=user_sites)
                
                # 해당 사이트들의 winch_serial_number 수집
                winch_objects = []
                for site in sites:
                    if site.winch_serial_number:
                        winch_objects.append(site.winch_serial_number)
                
                if winch_objects:
                    queryset = queryset.filter(winch_serial_number__in=winch_objects)
                else:
                    # 할당된 사이트에 연결된 winch가 없으면 빈 queryset 반환
                    queryset = queryset.none()
            except Exception:
                # 오류 발생 시 빈 queryset 반환
                queryset = queryset.none()
        
        return queryset


admin.site.register(Winch, WinchAdmin)
admin.site.register(WinchDataLog, WinchDataLogAdmin)
