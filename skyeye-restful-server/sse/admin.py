from django.contrib import admin
from django_eventstream.models import *


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'id', 'channel', 'data', 'user', 'created')
    list_filter = ('channel', 'user')


class EventCounterAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = (
        'id', 'name', 'value', 'updated')


admin.site.register(Event, EventAdmin)
admin.site.register(EventCounter, EventCounterAdmin)
