from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter
from rest_framework import filters, generics, permissions, response, status, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import RateSerializer, UserSerializer
from api.services import create_user
from rates.models import Rate

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Получение токена аутентификации по email и password', tags=['Users'],
                       responses={201: OpenApiResponse(description='OK', response=TokenObtainPairSerializer),
                                  400: OpenApiResponse(description='Provided data is invalid')}),
)
class LoginView(TokenObtainPairView):
    """Получение токена аутентификации по email и password."""


class RegisterView(views.APIView):
    """Регистрация и активация пользователя."""

    @extend_schema(request=UserSerializer, tags=['Users'], summary='Регистрация и активация пользователя',
                   responses={201: OpenApiResponse(description='Created'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)
        return response.Response(status=status.HTTP_201_CREATED)


class RateView(generics.ListAPIView):
    """Получение последних загруженных котировок."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):  # для drf-spectacular
        return RateSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):  # для drf-spectacular
            return Rate.objects.none()
        return Rate.objects.all()

    @extend_schema(tags=['Rates'], summary='Получение последних загруженных котировок',
                   parameters=[OpenApiParameter(name='order_by', type=str, enum=['value', '-value'])],
                   responses={201: OpenApiResponse(response=RateSerializer(many=True), description='OK'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def get(self, request):
        query = request.query_params['order_by']
        rates = self.get_queryset().order_by(query if query in ['value', '-value'] else 'value')
        serializer = self.get_serializer_class()(rates, many=True)
        return response.Response(serializer.data)
