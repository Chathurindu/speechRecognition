from django.apps import AppConfig


class AppRecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_records'

    def ready(self):
        import app_records.signals

