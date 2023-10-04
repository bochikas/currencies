from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import response, status, views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import UserSerializer
from api.services import create_user

User = get_user_model()


@extend_schema_view(
    post=extend_schema(description='Получение токена аутентификации по email и password', tags=['Users'],
                       responses={201: OpenApiResponse(description='OK', response=TokenObtainPairSerializer),
                                  400: OpenApiResponse(description='Provided data is invalid')}),
)
class LoginView(TokenObtainPairView):
    """Получение токена аутентификации по email и password."""


class CreateUserView(views.APIView):
    """Регистрация и активация пользователя."""

    @extend_schema(request=UserSerializer, tags=['Users'],
                   responses={201: OpenApiResponse(description='Created'),
                              400: OpenApiResponse(description='Provided data is invalid')})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)
        return response.Response(status=status.HTTP_201_CREATED)
