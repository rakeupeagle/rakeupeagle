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

def test_about(anon_client):
    path = reverse('about')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_faq(anon_client):
    path = reverse('faq')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_privacy(anon_client):
    path = reverse('privacy')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_team(anon_client):
    path = reverse('team')
    response = anon_client.get(path)
    assert response.status_code == 200

def test_robots(anon_client):
    path = reverse('robots')
    response = anon_client.get(path)
    assert response.status_code == 200

@pytest.mark.django_db
def test_sitemap(anon_client):
    path = reverse('sitemap')
    response = anon_client.get(path)
    assert response.status_code == 200
