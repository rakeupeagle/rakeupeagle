# Django
# Third-Party
import pytest

from django.urls import reverse


def test_deploy():
    assert True


def test_index(anon_client):
    path = reverse('index')
    response = anon_client.get(path)
    assert response.status_code == 200

# def test_recipients(anon_client):
#     path = reverse('recipients')
#     response = anon_client.get(path)
#     assert response.status_code == 200
