import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken

from rates.models import Rate, Currency, UserCurrency

User = get_user_model()


@pytest.fixture(autouse=True, scope="function")
def reset_cache():
    yield
    cache.clear()


@pytest.fixture
def user_data():
    return {'email': 'test@example.com', 'password': 'testpassword123'}


@pytest.fixture
def wrong_user_data():
    return {'email': 'test_user', 'password': 'short'}


@pytest.fixture
def user(user_data):
    user = User.objects.create(email=user_data['email'])
    user.set_password(user_data['password'])
    user.save()
    return user


@pytest.fixture
def user_token(user):
    refresh = RefreshToken.for_user(user)

    return str(refresh.access_token)


@pytest.fixture
def user_client(user_token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    return client


@pytest.fixture
def currency():
    return Currency.objects.create(char_code='USD', name='Доллар США')


@pytest.fixture
def rate(currency):
    return Rate.objects.create(currency=currency, date='2023-10-09', value='99.2')


@pytest.fixture
def user_currency(user, currency):
    return UserCurrency.objects.create(threshold=100, user=user, currency=currency)


@pytest.fixture
def user_currency_data(user, currency):
    return {'user': user.id, 'currency': currency.id, 'threshold': '100.0'}
