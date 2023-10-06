import datetime

import requests
from celery import shared_task
from django.conf import settings

from rates.models import Rate


class CBRConnectionException(Exception):
    pass


@shared_task(ignore_result=True, autoretry_for=(CBRConnectionException,), retry_backoff=True)
def load_currency_rates():
    """Загрузка дневных котировок ЦБ РФ."""

    url = settings.CBR_DAILY_RATES_URL
    today = datetime.date.today()
    to_create = list()
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
            to_create.append(Rate(date=today, char_code=key, value=value.get('Value')))

        today = today - datetime.timedelta(days=1)
        url = all_rates.get('PreviousURL').strip('\\/').replace('\\/', '/').replace('www.', 'https://')

    Rate.objects.bulk_create(to_create)
