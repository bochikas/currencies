import datetime

import requests
from celery import shared_task
from django.conf import settings
from django.db import transaction

from rates.models import Currency, Rate


class CBRConnectionException(Exception):
    pass


@shared_task(ignore_result=True, autoretry_for=(CBRConnectionException,), retry_backoff=True)
def load_currency_rates():
    """Загрузка дневных котировок ЦБ РФ за последние 30 дней."""

    url = settings.CBR_DAILY_RATES_URL
    today = datetime.date.today()
    to_create = list()
    to_update = list()

    with transaction.atomic():
        for _ in range(30):
            if Rate.objects.filter(date=today).exists():
                today = today - datetime.timedelta(days=1)
                continue

            response = requests.get(url=url)
            if response.status_code != 200:
                raise CBRConnectionException(response.content.decode('utf-8'))

            all_rates = response.json()
            currency_values = all_rates.get('Valute')
            for key, value in currency_values.items():
                currency, _ = Currency.objects.get_or_create(char_code=key.upper())
                to_create.append(Rate(date=today, currency=currency, value=value.get('Value')))
                if not currency.name:
                    currency.name = value.get('Name')
                    to_update.append(currency)

            today = today - datetime.timedelta(days=1)
            url = all_rates.get('PreviousURL').strip('\\/').replace('\\/', '/').replace('www.', 'https://')

        Rate.objects.bulk_create(to_create)
        Currency.objects.bulk_update(to_update, fields=['name'])
