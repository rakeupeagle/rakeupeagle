import sentry_sdk
from django.apps import AppConfig
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration


class AppConfig(AppConfig):
    name = 'app'
    default_auto_field = 'hashid_field.HashidAutoField'
    def ready(self):
        sentry_sdk.init(
            integrations=[
                DjangoIntegration(
                    transaction_style='function_name',
                ),
                RedisIntegration(),
                RqIntegration(),
            ],
            **settings.SENTRY_CONFIG,
        )
