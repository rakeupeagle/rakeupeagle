# Django
# First-Party
import pytest
from app.factories import AccountFactory
from app.factories import UserFactory
from django.test.client import Client


@pytest.fixture
def anon_client():
    client = Client()
    return client


@pytest.fixture
def user_client():
    user = UserFactory(
        username='user',
        name='User',
        email='user@dbinetti.com',
        is_active=True,
        is_admin=False,
    )
    AccountFactory(
        user=user,
    )
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def admin_client():
    admin = UserFactory(
        username='admin',
        name='Admin',
        email='admin@dbinetti.com',
        is_active=True,
        is_admin=True,
    )
    client = Client()
    client.force_login(admin)
    return client
