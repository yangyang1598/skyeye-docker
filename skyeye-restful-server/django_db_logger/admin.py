from __future__ import unicode_literals
import logging

from django.contrib import admin
from django.utils.html import format_html

from django_db_logger.config import DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
from .models import StatusLog


class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('create_datetime', 'colored_level', 'logger_name', 'msg', 'traceback')
    list_display_links = ('create_datetime', )
    list_filter = ('level', 'logger_name')
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE

    def colored_level(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'

        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=self.switch(instance.level))
    colored_level.short_description = 'Level'

    def switch(self, key):
        level = {10: "DEBUG", 20: "INFO", 30: "WARNING", 40: "ERROR", 50: "CRITICAL"}.get(key, "NONE")
        return level

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')

    def create_datetime_format(self, instance):
        return instance.create_datetime.strftime('%Y-%m-%d %X')
    create_datetime_format.short_description = 'Created at'


admin.site.register(StatusLog, StatusLogAdmin)