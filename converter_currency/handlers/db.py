import json

from aiohttp.web import json_response, Request
from pydantic import BaseModel, ValidationError, validator


class _DataBaseQueryData(BaseModel):
    """ Storage and validation data of post query /database?... """
    merge: int

    @validator('merge')
    def merge_should_be_one_or_zero(cls, merge: int) -> int:
        if merge not in [0, 1]:
            raise ValueError('merge should be one or zero')

        return merge


class DBCurrencyHandler:
    """ Handler to /database """
    def __init__(self, currency_storage):
        self.currency_storage = currency_storage

    async def post(self, request: Request):
        data = await request.content.read()
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            return json_response({f'{type(e).__name__}': str(e)}, status=400)

        params = request.query
        try:
            data_base_query_data = _DataBaseQueryData(**params)
        except ValidationError as e:
            return json_response(e.json(), status=400)

        await self.currency_storage.update(data, data_base_query_data.merge)

        return json_response({'result': 'OK'})
