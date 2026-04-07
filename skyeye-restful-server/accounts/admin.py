from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from accounts.models import NotificationUser, User


def apply_help_texts(form):
    if "username" in form.fields:
        form.fields["username"].help_text = format_html(
            "● 필수 입력 사항입니다.<br>● 150자 이내로 작성해 주세요.<br>● 문자, 숫자, @/./+/-/_만 사용 가능합니다."
        )
    if "password1" in form.fields:
        form.fields["password1"].help_text = format_html(
            "● 비밀번호는 ID와 유사하게 설정할 수 없습니다.<br>● 비밀번호는 최소 8자여야 합니다.<br>● 연속적인 숫자처럼 추측하기 쉬운 비밀번호는 사용할 수 없습니다.<br>● 비밀번호는 숫자로만 구성될 수 없습니다."
        )
    if "password2" in form.fields:
        form.fields["password2"].help_text = "비밀번호를 확인하세요."
    if "is_staff" in form.fields:
        form.fields["is_staff"].help_text = "이 항목을 선택하지 않으면 웹 페이지 접속이 제한되며, API를 통한 서비스 이용만 가능합니다."
    if "is_active" in form.fields:
        form.fields["is_active"].help_text = "계정 활성화 여부입니다. 해제 시 로그인 및 서비스 이용이 제한됩니다."
    if "is_superuser" in form.fields:
        form.fields["is_superuser"].help_text = "이 사용자에게 명시적으로 권한을 부여하지 않고도 모든 권한을 갖도록 지정합니다."
    if "groups" in form.fields:
        form.fields["groups"].help_text = "이 사용자가 속한 그룹 목록입니다. 사용자는 각 그룹에 부여된 모든 권한을 갖게 됩니다."


class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name","last_name", "password1", "password2", "groups", "is_staff", "is_active", "is_superuser")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        manage_group = Group.objects.filter(name="Manage").first()
        if manage_group and "groups" in self.fields:
            self.fields["groups"].initial = [manage_group.pk]
        apply_help_texts(self)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            manage_group = Group.objects.filter(name="Manage").first()
            if manage_group:
                user.groups.add(manage_group)
        return user


class AccountChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_help_texts(self)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"


class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('username', 'first_name','last_name', 'last_login', 'is_active', 'is_staff')
    search_fields = ('username',)
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
