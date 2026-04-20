from django.apps import AppConfig
import threading

class SseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sse'

class YourAppConfig(AppConfig):
    name = 'yourapp'

    def ready(self):
        from .heartbeat import heartbeat_loop

        threading.Thread(target=heartbeat_loop, daemon=True).start()