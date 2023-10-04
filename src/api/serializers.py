from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import validate_password

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
