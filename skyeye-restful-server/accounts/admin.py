from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponseRedirect

from accounts.models import NotificationUser, User


class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name","last_name", "password1", "password2", "groups", "is_staff", "is_active", "is_superuser")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manage_group = Group.objects.filter(name="Manage").first()
        if manage_group and "groups" in self.fields:
            self.fields["groups"].initial = [manage_group.pk]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            manage_group = Group.objects.filter(name="Manage").first()
            if manage_group:
                user.groups.add(manage_group)
        return user


class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('username', 'first_name','last_name', 'last_login', 'is_active', 'is_staff')
    search_fields = ('username')
    readonly_fields = ('id', 'last_login')

    add_form = AccountCreationForm
    form = AccountChangeForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name","last_name", "password1", "password2", "is_superuser", "groups", "is_staff", "is_active"),
            },
        ),
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("is_superuser", "first_name","last_name", "groups", "is_staff", "is_active"),
            },
        ),
    )

    filter_horizontal = ()
    list_filter = ()

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse("admin:accounts_user_changelist"))


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
