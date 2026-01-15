from django.apps import AppConfig
from server import settings


class MissionDeviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mission_device'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from notification import send
            send.start()