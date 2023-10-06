from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='v1-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='v1-schema'), name='v1-docs'),
    path('user/', include('api.urls.v1_users_urls')),
    path('rates/', include('api.urls.v1_rates_urls')),
    path('currency/', include('api.urls.v1_currency_urls')),
]
