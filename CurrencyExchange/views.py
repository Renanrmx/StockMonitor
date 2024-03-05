# from django.shortcuts import render
import json

from ninja.errors import HttpError
import requests
import yfinance as yf


def currency_exchange(source, target, amount):

    # TODO: Mover ou utilizar banco de dados
    allowed_currencies = {
        'USD': {'id': 'usd', 'type': 'common'},
        'BRL': {'id': 'brl', 'type': 'common'},
        'EUR': {'id': 'eur', 'type': 'common'},
        'BTC': {'id': 'bitcoin', 'type': 'crypto'},
        'ETH': {'id': 'ethereum', 'type': 'crypto'}
    }

    exchange_rate = 0
    backing = 'usd'

    if source.upper() == target:
        raise HttpError(400, "A moeda de destino não pode ser igual a de origem.")

    if (source in allowed_currencies) and (target in allowed_currencies):
        source_value = allowed_currencies[source]
        target_value = allowed_currencies[target]

        # Por ser uma API paga com limite gratuito limitei a só utilizar para criptomoedas por economia

        if source_value['type'] == 'common' and target_value['type'] == 'common':
            exchange_rate = get_common_currency_rate(source_value['id'], target_value['id'])

        elif source_value['type'] == 'crypto' and target_value['type'] == 'crypto':
            source_dolar = get_crypto_currency_rate(source_value['id'], backing)
            target_dolar = get_crypto_currency_rate(target_value['id'], backing)
            exchange_rate = source_dolar / target_dolar

        elif source_value['type'] == 'crypto' and target_value['type'] == 'common':
            source_dolar = get_crypto_currency_rate(source_value['id'], backing)
            target_rate = get_common_currency_rate(backing, target_value['id'])
            exchange_rate = target_rate * source_dolar

        elif source_value['type'] == 'common' and target_value['type'] == 'crypto':
            source_rate = get_common_currency_rate(source_value['id'], backing)
            target_dolar = get_crypto_currency_rate(target_value['id'], backing)
            exchange_rate = source_rate / target_dolar

    else:
        raise HttpError(400, "Moeda solicitada não disponível.")

    return exchange_rate * amount


def get_common_currency_rate(source, target):
    """ Taxa de cambio entre moedas governamentais comuns """

    try:
        return yf.download(f'{source}{target}=X')['Close'].iloc[-1]
    except:
        raise HttpError(503, "Serviço de conversão temporariamente indisponível. Tente novamente mais tarde.")


def get_crypto_currency_rate(source, target):
    """ Taxa de cambio entre moedas porém o target não aceita todas, dar preferencia a USD """

    base_url = 'https://api.coingecko.com/api/v3/simple/price'
    response = requests.get(f'{base_url}?ids={source}&vs_currencies={target}')

    if response.status_code == 200:
        data = response.json()
        # Acessa o valor de câmbio no dicionário retornado
        return data[source][target]
    else:
        raise HttpError(503, "Serviço de conversão temporariamente indisponível. Tente novamente mais tarde.")
