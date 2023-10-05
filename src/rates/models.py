from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Rate(models.Model):
    """Курс валюты."""

    char_code = models.CharField(verbose_name='код валюты', max_length=3)
    date = models.DateField(verbose_name='дата')
    value = models.DecimalField(verbose_name='курс', max_digits=10, decimal_places=4)

    class Meta:
        verbose_name = 'курс валют'
        verbose_name_plural = 'курсы валют'
        ordering = ('-date',)


class UserCurrency(models.Model):
    """Отслеживаемые валюты пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='currencies')
    currency = models.ForeignKey(Rate, on_delete=models.CASCADE, verbose_name='курс валюты')
    threshold = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='порог')

    class Meta:
        verbose_name = 'отслеживаемая валюта'
        verbose_name_plural = 'отслеживаемые валюты'
        ordering = ('id',)
