import json

from tests_currency_converter import convert_to_json, cli


async def test_post_when_merge_not_one_or_zero_then_return_json_with_exception(cli):
    response = await cli.post('/database?merge=2', data=json.dumps({'EUR': 100}))
    _json = await convert_to_json(response)
    assert response.status == 400


async def test_post_when_merge_one_then_return_json_with_result_ok(cli):
    response = await cli.post('/database?merge=1', data=json.dumps({'EUR': 100}))
    _json = await convert_to_json(response)
    assert _json['result'] == 'OK'
    assert response.status == 200


async def test_post_when_merge_zero_then_return_json_with_result_ok(cli):
    response = await cli.post('/database?merge=0', data=json.dumps({'EUR': 100}))
    _json = await convert_to_json(response)
    assert _json['result'] == 'OK'
    assert response.status == 200


async def test_post_when_data_str_not_json_then_return_json_with_exception_msg(cli):
    response = await cli.post('/database?merge=0', data='not json')
    _json = await convert_to_json(response)
    assert 'JSONDecodeError' in _json
    assert response.status == 400
