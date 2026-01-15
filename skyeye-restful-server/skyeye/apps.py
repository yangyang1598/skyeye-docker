from django.apps import AppConfig


class SkyeyeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skyeye'

    def ready(self):
        import skyeye.signals  # signals 등록