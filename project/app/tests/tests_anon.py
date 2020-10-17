# Django
from django.urls import reverse

# First-Party
import pytest


def test_deploy():
    assert True


def test_index(anon_client):
    path = reverse('index')
    response = anon_client.get(path)
    assert response.status_code == 200
