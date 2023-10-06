from django.urls import path

from api.views import RateView


urlpatterns = [
    path('', RateView.as_view(), name='v1-rates'),
]
