import sentry_sdk
from django.apps import AppConfig
from django.conf import settings


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        sentry_sdk.init(**settings.SENTRY_CONFIG)
        import app.signals
