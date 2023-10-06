from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import validate_password
from rates.models import Rate, UserCurrency

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователей."""

    email = serializers.EmailField(validators=[
        UniqueValidator(queryset=User.objects.all(), message='Пользователь с таким email уже зарегистрирован')
    ])

    def validate_password(self, value):
        return validate_password(value, User)

    class Meta:
        model = User
        fields = ('id', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class RateSerializer(serializers.ModelSerializer):
    """Сериализатор курсов валют."""

    class Meta:
        model = Rate
        fields = ('id', 'char_code', 'date', 'value')


class UserCurrencySerializer(serializers.ModelSerializer):
    """Сериализатор отслеживаемых валют."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserCurrency
        fields = ('user', 'currency', 'threshold')


class AnalyticsSerializer(serializers.ModelSerializer):
    """Сериализатор аналитики по валюте."""

    is_threshold_exceeded = serializers.BooleanField()
    threshold_match_type = serializers.CharField()
    is_min_value = serializers.BooleanField()
    is_max_value = serializers.BooleanField()
    percentage_ratio = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Rate
        fields = ('id', 'date', 'char_code', 'value', 'is_threshold_exceeded', 'threshold_match_type', 'is_min_value',
                  'is_max_value', 'percentage_ratio')
