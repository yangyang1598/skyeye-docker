from django.contrib import admin
from .models import Detection


class DetectionAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    # list_display = (
    #     'id', 'date', 'image', 'detection_rate', 'class_name', 'ai_model', 'user')
    list_display = (
        'id', 'date', 'site_id', 'class_name', 'ai_model', 'user')

admin.site.register(Detection, DetectionAdmin)
