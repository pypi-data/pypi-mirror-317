import pytest

from tests.Abc.BaseTest import BaseTest
from xync_client.Abc.Agent import BaseAgentClient
from xync_client.Abc.Base import BaseClient


class AgentTest(BaseTest):
    async def clients(self) -> list[BaseClient]:
        pass

    @pytest.fixture(scope="class", autouse=True)
    async def cl(self) -> BaseAgentClient:
        agent = (await self.ex).agents.filter(auth__not_isnull=True).first()
        acl = BaseClient(agent)
        yield acl
        await acl.close()
