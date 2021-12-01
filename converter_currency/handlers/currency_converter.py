
from aiohttp.web import json_response, Request
from pydantic import BaseModel, ValidationError, Field


class _ConvertQueryData(BaseModel):
    """ Storage and validation data of get query /convert?... """

    from_currency: str = Field(alias='from')
    to_currency: str = Field(alias='to')
    amount: float


class CurrencyConverter:
    """ Handler to /convert """
    def __init__(self, currency_storage):
        self._currency_storage = currency_storage

    async def convert(self, from_currency: str, to_currency: str, amount: float) -> float:
        from_rate_currency = await self._currency_storage.get(from_currency)
        to_rate_currency = await self._currency_storage.get(to_currency)
        return (from_rate_currency / to_rate_currency) * amount

    async def get(self, request: Request):
        params = request.query
        try:
            currency_data = _ConvertQueryData(**params)
        except ValidationError as e:
            return json_response(e.json(), status=400)

        try:
            result = await self.convert(currency_data.from_currency, currency_data.to_currency, currency_data.amount)
        except (ValueError, ZeroDivisionError) as e:
            return json_response({f'{type(e).__name__}': str(e)}, status=400)

        return json_response({'result': result}, status=200)
