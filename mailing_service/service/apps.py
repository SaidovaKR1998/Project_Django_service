from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'

    def ready(self):
        # Закомментируйте эту строку:
        # from . import scheduler
        # scheduler.start_scheduler()
        pass  # Добавьте эту строку