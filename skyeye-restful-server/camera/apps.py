from django.apps import AppConfig
from server import settings

class CameraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'camera'
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from camera import delete_daliy
            delete_daliy.start()