# Django
from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'
    def ready(self):
        pass
        # from .signals import user_post_delete, user_post_save
