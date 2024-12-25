import pytest

from xync_client.Abc.Base import BaseClient
from xync_client.Abc.BaseTest import BaseTest


class AgentTest(BaseTest):
    @pytest.fixture(scope="class", autouse=True)
    async def cl(self) -> BaseClient:
        agent = (await self.exq).agents.filter(auth__not_isnull=True).first()
        acl = BaseClient(agent)
        yield acl
        await acl.close()
