import decimal

from django.contrib.auth import get_user_model

from rates.models import Rate, UserCurrency

User = get_user_model()


def create_user(*, password: str, email: str = '') -> None:
    """Создание пользователя."""

    user = User(email=email)
    user.set_password(password)
    user.save()


def create_user_currency(*, user: User, currency: Rate, threshold: decimal.Decimal) -> None:
    """Добавление отслеживаемой валюты."""

    UserCurrency.objects.get_or_create(user=user, currency=currency, threshold=threshold)
