# Django
# First-Party
import pytest
from app.factories import UserFactory
from django.test.client import Client


@pytest.fixture
def anon_client():
    client = Client()
    return client


@pytest.fixture
def user_client():
    user = UserFactory(
        name='User',
        phone='+15005551212',
        is_active=True,
        is_admin=False,
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def admin_client():
    admin = UserFactory(
        name='Admin',
        phone='+15005551212',
        is_active=True,
        is_admin=True,
    )
    client = Client()
    client.force_login(admin)
    return client
