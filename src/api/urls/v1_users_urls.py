from django.urls import path

from api.views import RegisterView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='v1-users-register'),
    path('login/', LoginView.as_view(), name='v1-users-login'),
]
