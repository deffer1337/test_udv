from typing import List

from aiohttp.web import get, post
from aioredis import Redis

from converter_currency.handlers.currency_converter import CurrencyConverter
from converter_currency.models.currency_storage import CurrencyStorage
from converter_currency.handlers.db import DBCurrencyHandler


def create_routes(redis_connection: Redis) -> List:
    """" 
    Building dependencies for handlers of routes 
    
    :param redis_connection: Need redis connection
    """""
    currency_storage = CurrencyStorage(redis_connection=redis_connection)
    currency_converter = CurrencyConverter(currency_storage)
    db_currency_handler = DBCurrencyHandler(currency_storage)
    routes = [get('/convert', currency_converter.get),
              post('/database', db_currency_handler.post)]

    return routes