from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Пользователь."""

    username = models.CharField(verbose_name=_('username'), max_length=150, null=True, blank=True)
    email = models.EmailField(verbose_name=_('email address'), unique=True)
    register_date = models.DateField(verbose_name='Дата регистрации', auto_now_add=True)
    deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        ordering = ('email',)
