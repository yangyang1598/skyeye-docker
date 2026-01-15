from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
from django.contrib.admin.models import LogEntry

class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class NotificationAdmin(admin.ModelAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('name', 'site_id','phone_number')
    
    search_fields = ['site_id__site_id']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'object_repr', 'change_message')
    list_filter = ('action_time', 'user')
    search_fields = ('object_repr', 'change_message')
    ordering = ('-action_time',)


admin.site.register(User, AccountAdmin)
admin.site.register(NotificationUser, NotificationAdmin)
