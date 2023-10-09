from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import F, Min, Max, Case, When, Value, functions, CharField
from django.db.models.lookups import Exact, LessThan
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from rest_framework import filters, generics, permissions, response, status, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api import serializers as api_serializers
from api.filters import RateFilter
from api.services import create_user, create_user_currency
from api.utils import cache_per_user
from rates.models import Rate, UserCurrency

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Получение токена аутентификации по email и password', tags=['Users'],
                       responses={200: OpenApiResponse(description='OK', response=TokenObtainPairSerializer),
                                  400: OpenApiResponse(description='Provided data is invalid')}),
)
class LoginView(TokenObtainPairView):
    """Получение токена аутентификации по email и password."""


class RegisterView(views.APIView):
    """Регистрация и активация пользователя."""

    @extend_schema(request=api_serializers.UserSerializer, tags=['Users'],
                   summary='Регистрация и активация пользователя',
                   responses={201: OpenApiResponse(description='Created'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def post(self, request):
        serializer = api_serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)
        return response.Response(status=status.HTTP_201_CREATED)


class RateView(generics.ListAPIView):
    """Получение последних загруженных котировок."""

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['value']

    def get_serializer_class(self):  # для drf-spectacular
        if not self.request.user.is_authenticated:
            return api_serializers.RateSerializerAnonym
        return api_serializers.RateSerializerAuthenticated

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # для drf-spectacular
            return Rate.objects.none()

        qs = Rate.objects.select_related('currency')
        last_rate = Rate.objects.latest('date')

        if last_rate:
            qs = qs.filter(date=last_rate.date)

        if not self.request.user.is_authenticated:
            return qs
        return qs.filter(currency__usercurrency__user=self.request.user).annotate(
            is_threshold_exceeded=LessThan(F('currency__usercurrency__threshold'), F('value')),
        )

    @method_decorator(cache_per_user(60*60*12))
    @extend_schema(tags=['Rates'], summary='Получение последних загруженных котировок',
                   parameters=[OpenApiParameter(name='order_by', type=str, enum=['value', '-value'])],
                   responses={200: OpenApiResponse(response=api_serializers.RateSerializerAnonym(many=True),
                                                   description='OK'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def get(self, request):
        rates = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer_class()(rates, many=True)
        return response.Response(serializer.data)


class UserCurrencyView(generics.CreateAPIView):
    """Добавление котируемой валюты в список отслеживаемых с установкой порогового значения."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return api_serializers.UserCurrencySerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # для drf-spectacular
            return UserCurrency.objects.none()
        return UserCurrency.objects.all()

    @extend_schema(tags=['Currency'],
                   summary='Добавление котируемой валюты в список отслеживаемых с установкой порогового значения',
                   responses={201: OpenApiResponse(description='OK'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        create_user_currency(**serializer.validated_data)
        return response.Response(status=status.HTTP_201_CREATED)


class UserCurrencyAnalyticsView(generics.RetrieveAPIView):
    """Получение аналитических данных по котируемой валюте за период."""

    permission_classes = [permissions.IsAuthenticated]
    filterset_class = RateFilter

    def get_serializer_class(self):
        return api_serializers.AnalyticsSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rate.objects.none()
        return Rate.objects.select_related('currency')

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        min_val, max_val = queryset.aggregate(
            min_value=Min('value'),
            max_value=Max('value')
        ).values()

        queryset = queryset.annotate(
            is_max_value=Exact(F('value'), max_val),
            is_min_value=Exact(F('value'), min_val),
        )

        query_threshold = self.request.query_params.get('threshold')
        if query_threshold:
            threshold = Decimal(query_threshold)
            queryset = queryset.annotate(
                is_threshold_exceeded=LessThan(F('value'), threshold),
                percentage_ratio=functions.Concat(
                    functions.Round(100 * threshold / F('value'), precision=2), Value('%'), output_field=CharField()
                ),
                threshold_match_type=Case(
                    When(value__gt=threshold, then=Value('Котировка меньше ПЗ')),
                    When(value__lt=threshold, then=Value('Котировка превысила ПЗ')),
                    default=Value('Котировка равна ПЗ'),
                )
            )
        else:
            queryset = queryset.annotate(
                threshold_match_type=Value('Значение не указано'),
                is_threshold_exceeded=Value(None),
                percentage_ratio=Value('%'),
            )

        return queryset

    @extend_schema(tags=['Currency'], filters=True,
                   summary='Получение аналитических данных по котируемой валюте за период',
                   responses={200: OpenApiResponse(description='OK', response=api_serializers.AnalyticsSerializer),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def get(self, request, id=None):
        rates = self.filter_queryset(self.get_queryset().filter(currency_id=id))
        serializer = self.get_serializer_class()(rates, many=True)
        return response.Response(serializer.data)
