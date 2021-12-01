
import pytest
from aiohttp import web, ContentTypeError

from currency_storage_mock import StorageMock
from converter_currency.routes import create_routes


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    routes = create_routes(StorageMock())
    app.add_routes(routes)
    return loop.run_until_complete(aiohttp_client(app))


async def convert_to_json(response):
    try:
        json = await response.json()
        return json
    except ContentTypeError as e:
        pytest.fail(f'{e}. Should be return JSON')


async def test_get_when_empty_quey_then_return_json_with_exception_msg(cli):
    response = await cli.get('/convert')
    await convert_to_json(response)

    assert response.status == 400


async def test_get_when_quey_with_not_exist_currency_then_return_json_with_exception_msg(cli):
    fr = 'BOB'
    to = 'RUR'
    response = await cli.get(f'/convert?from={fr}&to={to}&amount=42')
    json = await convert_to_json(response)
    exception = 'Currency {} not exists'
    assert json['ValueError'] == exception.format(fr) or json['ValueError'] == exception.format(to)
    assert response.status == 400
