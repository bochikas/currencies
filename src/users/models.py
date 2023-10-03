from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь."""

    register_date = models.DateField(verbose_name='Дата регистрации', auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
