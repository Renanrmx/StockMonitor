from django.urls import path

from CurrencyExchange.api import api


urlpatterns = [
    path("api/", api.urls),
]
