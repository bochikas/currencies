import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register_user(client, user_data, wrong_user_data):
    url = reverse('v1-users-register')
    response = client.post(url, user_data)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(url, wrong_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_user(client, user_data, user, wrong_user_data):
    url = reverse('v1-users-login')
    response = client.post(url, user_data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

    response = client.post(url, wrong_user_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
