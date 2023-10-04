from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rest_framework import serializers


def validate_password(password, model):
    """Валидация пароля."""

    try:
        password_validation.validate_password(password=password, user=model)
    except ValidationError as e:
        raise serializers.ValidationError(e)
    return password
