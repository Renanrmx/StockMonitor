from django.http import HttpResponse
from ninja import NinjaAPI
import numpy as np

from .views import *

api = NinjaAPI(csrf=True)


@api.get("/exchange")
def exchange(request, source: str, to: str, amount: float):
    exchange_result = currency_exchange(source.upper(), to.upper(), amount)
    return {"result": np.format_float_positional(exchange_result)}
