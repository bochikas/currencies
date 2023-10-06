from django.urls import path

from api.views import RegisterView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='v1-users-create-user'),
    path('login/', LoginView.as_view(), name='v1-users-login'),
]
