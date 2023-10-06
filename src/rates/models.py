from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Currency(models.Model):
    """Валюта."""

    char_code = models.CharField(verbose_name='код валюты', max_length=3)
    name = models.CharField(verbose_name='название', max_length=120)

    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'валюты'
        ordering = ('char_code',)


class Rate(models.Model):
    """Курс валюты."""

    date = models.DateField(verbose_name='дата')
    value = models.DecimalField(verbose_name='курс', max_digits=10, decimal_places=4)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates', verbose_name='валюта')

    class Meta:
        verbose_name = 'курс валют'
        verbose_name_plural = 'курсы валют'
        ordering = ('-date',)


class UserCurrency(models.Model):
    """Отслеживаемые валюты пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='currencies')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='курс валюты')
    threshold = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='порог')

    class Meta:
        verbose_name = 'отслеживаемая валюта'
        verbose_name_plural = 'отслеживаемые валюты'
        ordering = ('id',)
