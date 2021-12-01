import pytest

from converter_currency.models.currency_storage import CurrencyStorage
from currency_storage_mock import StorageMock


class TestCurrencyStorage:
    def setup_class(self):
        self.currency_storage = CurrencyStorage(StorageMock())

    @pytest.mark.asyncio
    async def test_get_when_currency_RUR_than_return_one(self):
        assert await self.currency_storage.get('RUR') == 1

    @pytest.mark.asyncio
    async def test_get_when_currency_not_exists_than_raise_value_error(self):
        with pytest.raises(ValueError) as exception:
            currency = 'BOB'
            await self.currency_storage.get(currency)

        assert str(exception.value) == f'Currency {currency} not exists'

    @pytest.mark.asyncio
    async def test_get_when_currency_exists_then_return_rate_currency(self):
        await self.currency_storage.update({'USD': 60.0}, True)
        assert await self.currency_storage.get('USD') == 60.0

    @pytest.mark.asyncio
    async def test_update_when_merge_false_then_old_data_should_be_removed(self):
        await self.currency_storage.update({'USD': 60.0, 'EUR': 20}, True)
        await self.currency_storage.update({'RUR': 120.0}, False)
        assert list(self.currency_storage._redis.db.keys()) == ['RUR']

    @pytest.mark.asyncio
    async def test_update_when_merge_true_then_old_data_should_be_save(self):
        await self.currency_storage.update({'USD': 60.0, 'EUR': 20}, True)
        await self.currency_storage.update({'RUR': 120.0}, True)
        assert set(self.currency_storage._redis.db.keys()) == {'USD', 'EUR', 'RUR'}

    @pytest.mark.asyncio
    async def test_update_when_merge_true_and_currency_exists_in_db_then_old_currency_should_be_change(self):
        await self.currency_storage.update({'USD': 60.0}, True)
        await self.currency_storage.update({'USD': 120.0}, True)
        assert await self.currency_storage.get('USD') == 120.0

