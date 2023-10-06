from django.urls import path

from api.views import UserCurrencyView, UserCurrencyAnalyticsView

urlpatterns = [
    path('<int:id>/analytics/', UserCurrencyAnalyticsView.as_view(), name='v1-user-currency-analytics'),
    path('user_currency/', UserCurrencyView.as_view(), name='v1-user-currency'),
]
