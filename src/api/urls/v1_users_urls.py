from django.urls import path

from api import views


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='v1-users-create-user'),
    path('login/', views.LoginView.as_view(), name='v1-users-token-obtain'),
]
