# Django
from django.urls import reverse

# First-Party
import pytest


def test_deploy():
    assert True

@pytest.mark.django_db
def test_dashboard(user_client):
    response = user_client.get(reverse('dashboard'))
    assert response.status_code == 200

# @pytest.mark.django_db
# def test_parent(user_client):
#     response = user_client.get(reverse('parent'))
#     assert response.status_code == 200
#     response = user_client.post(
#         reverse('parent'),
#         {
#             'students-TOTAL_FORMS': '5',
#             'students-INITIAL_FORMS': '1',
#             'students-MIN_NUM_FORMS': '0',
#             'students-MAX_NUM_FORMS': '5',
#             'students-0-name': 'Foo Student',
#             'students-0-school': 'Brittan Acres',
#             'students-0-grade': '2 Grade',
#         }
#     )
#     assert response.context == 200
