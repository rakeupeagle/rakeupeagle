# Django
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from app.models import User
from app.tasks import auth0_get_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(
            email__endswith='@startnormal.com',
        )
        users.delete()
        client = auth0_get_client()
        accounts = client.users.list(q='*@startnormal.com')
        us = accounts['users']
        for u in us:
            client.users.delete(u['user_id'])
        self.stdout.write("Complete.")
        return
