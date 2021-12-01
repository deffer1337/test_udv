from typing import Dict

from aioredis import Redis


class CurrencyStorage:
    def __init__(self, redis_connection: Redis):
        self._redis = redis_connection

    async def get(self, currency: str) -> float:
        """
        Getting the currency value
        If currency not exist then raise ValueError

        :param currency: String representation currency
        """
        if currency == 'RUR':
            return 1.0

        rate = await self._redis.get(currency.upper())
        if not rate:
            raise ValueError(f'Currency {currency} not exists')

        return float(rate.decode())

    async def update(self, data: Dict[str, float], merge: bool) -> None:
        """
        Update data in DB

        :param data: Dictionary with currency and her rate
        :param merge: If merge==false then in DB old data remove,
        else the old data is change over the new, but the old ones are still relevant, if not changed
        """
        if not merge:
            await self._redis.flushdb()

        for currency, rate in data.items():
            await self._redis.set(currency, rate)
