import pytest

from xync_client.Abc.Ex import BaseExClient
from xync_client.Abc.BaseTest import BaseTest


class ExTest(BaseTest):
    @pytest.fixture(scope="class", autouse=True)
    async def cl(self) -> BaseExClient:
        ecl = BaseExClient(await self.exq)
        yield ecl
        await ecl.close()
