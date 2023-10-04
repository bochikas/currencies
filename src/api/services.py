from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(*, password: str, email: str = '') -> None:
    """Создание пользователя."""

    user = User(email=email)
    user.set_password(password)
    user.save()
