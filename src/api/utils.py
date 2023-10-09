from functools import wraps

from django.views.decorators.cache import cache_page


def cache_per_user(timeout):
    """Декоратор для кеширования запросов с разделением по пользователям."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                prefix = f'_auth_user_{request.user.id}_'
            else:
                prefix = '_auth_user_anonym_'
            result = cache_page(timeout, key_prefix=prefix)
            return result(view_func)(request, *args, **kwargs)
        return wrapper
    return decorator
