from django.contrib import admin
from .models import *


# Register your models here.
class HelikiteAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'serial_number', 'cubic', 'type', 'weight', 'payload', 'production_year', 'image_file_path')


admin.site.register(Helikite, HelikiteAdmin)
