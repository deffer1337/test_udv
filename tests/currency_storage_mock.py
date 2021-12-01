

class StorageMock:
    def __init__(self):
        self.db = {}

    async def get(self, key: str) -> float:
        if key not in self.db:
            return None

        if key == 'RUR':
            return 1.0

        return self.db[key]

    async def flushdb(self):
        self.db.clear()

    async def set(self, key: str, value: float):
        self.db[key] = f'{value}'.encode()