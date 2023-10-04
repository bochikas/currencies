from django.urls import path

from api import views


urlpatterns = [
    path('', views.RateView.as_view(), name='v1-rates'),
]
