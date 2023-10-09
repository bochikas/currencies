import pytest
from django.urls import reverse
from rest_framework import status

from rates.models import UserCurrency


@pytest.mark.django_db
def test_create_user_currency(user_client, user_currency_data, client, user):
    url = reverse('v1-user-currency')
    cnt = UserCurrency.objects.filter(user=user).count()
    response = user_client.post(url, user_currency_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert UserCurrency.objects.filter(user=user).count() == cnt + 1

    response = client.post(url, user_currency_data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_rates(client, rate, user_client, user_currency):
    url = reverse('v1-rates')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'is_threshold_exceeded' not in response.data[0]

    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'is_threshold_exceeded' in response.data[0]
