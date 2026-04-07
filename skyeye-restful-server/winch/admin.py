import ast
import json

from django import forms
from django.contrib import admin
from .models import *
from skyeye.models import Site

# Register your models here.
class WinchAdminForm(forms.ModelForm):
    brake_operations = forms.MultipleChoiceField(
        choices=Winch.BrakeOperations.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'brake-operations-checkboxes'}),
    )

    class Meta:
        model = Winch
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raw = getattr(self.instance, 'brake_operations', None)
        selected = []
        if raw:
            if isinstance(raw, (list, tuple, set)):
                selected = list(raw)
            else:
                text = str(raw).strip()
                if text.startswith('[') and text.endswith(']'):
                    try:
                        parsed = json.loads(text)
                        if isinstance(parsed, list):
                            selected = parsed
                    except Exception:
                        try:
                            parsed = ast.literal_eval(text)
                            if isinstance(parsed, (list, tuple, set)):
                                selected = list(parsed)
                        except Exception:
                            selected = []
                if not selected:
                    selected = [part.strip() for part in text.split(',') if part.strip()]
        selected = [v.strip() for v in selected if v and str(v).strip()]
        self.initial['brake_operations'] = selected
        self.fields['brake_operations'].initial = selected

    def clean_brake_operations(self):
        selected = self.cleaned_data.get('brake_operations') or []
        selected = [v.strip() for v in selected if v and v.strip()]
        return None if not selected else ', '.join(selected)


class WinchAdmin(admin.ModelAdmin):
    form = WinchAdminForm

    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('serial_number', 'tetherline_length', 'router', 'brake_operations')
    fields = ('serial_number', 'tetherline_length', 'router', 'brake_operations')
    def get_readonly_fields(self, request, obj=None):
        return ('serial_number',) if obj else ()

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
