# Stock Monitor

Projeto de demonstração em Django 5 e API Ninja

Inicialmente criado somente o app de conversão monetária, em breve como o nome sugere será implementado um monitor de ações de bolsas de valores

## APP Currency Converter

API em Django Ninja para conversão monetária

Admin não implementado

## Pré requisitos (Docker)

* Na pasta raiz do projeto executar:
```docker build -t stock-monitor .```

* Em seguida ao completar iniciar o container:
```docker run -p 8000:8000 stock-monitor```

## Pré requisitos (Manual)

* Intalar o Python 3.11 ou superior

* Executar o requirements.txt com o comando ```pip install -r requirements.txt```

* Iniciar o projeto com o comando ```python manage.py runserver```

# Utilização

* A API poderá ser consumida como no exemplo: 
```http://localhost:8000/api/exchange?source=USD&to=BRL&amount=105.30``` seguindo o padrão US de separação com ponto ao invés de vírgula

* Documentação dinâmica: 
```http://localhost:8000/api/docs#/default/CurrencyExchange_api_exchange```

---

Obs 1: Valores podem variar um pouco ao comparar entre sistemas por conta de delay proposital.

Obs 2: Número resultante em string para não perder precisão.

---

Até o momento está limitado às seguintes moedas:
```USD, BRL, EUR, BTC, ETH```
