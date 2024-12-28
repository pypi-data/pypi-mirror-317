import logging

import pytest
from xync_schema.enums import ExStatus, ExType, ExAction
from xync_schema.models import Ex, TestEx as TestExs

from tests.Abc.BaseTest import BaseTest
from xync_client.Abc.Base import BaseClient, DictOfDicts, FlatDict
from xync_client.Abc.Ex import BaseExClient


class TestEx(BaseTest):
    @pytest.fixture(scope="class")
    async def clients(self) -> list[BaseClient]:
        exs = await Ex.filter(status__gt=ExStatus.plan)
        [await ex.fetch_related("agents") for ex in exs if ex.type_ == ExType.tg]
        clients: list[BaseExClient] = [ex.client() for ex in exs]
        yield clients
        [await cl.close() for cl in clients]

    # 20
    async def test_pms(self, clients: list[BaseExClient]):
        for client in clients:
            pms: DictOfDicts = await client.pms()
            t, _ = await TestExs.update_or_create({"ok": self.is_dict_of_dicts(pms)}, ex=client.ex, action=ExAction.pms)
            assert t.ok, "No pms"
            logging.info(f"{client.ex.name}:{ExAction.pms.name} - ok")

    # 21
    async def test_curs(self, clients: list[BaseExClient]):
        for client in clients:
            curs: FlatDict = await client.curs()
            t, _ = await TestExs.update_or_create({"ok": self.is_flat_dict(curs)}, ex=client.ex, action=ExAction.curs)
            assert t.ok, "No curs"
            logging.info(f"{client.ex.name}:{ExAction.pms.name} - ok")

    # 22
    async def test_cur_pms_map(self, clients: list[BaseExClient]):
        for client in clients:
            cur_pms: DictOfDicts = await client.cur_pms_map()
            ok = self.is_dict_of_dicts(cur_pms)
            t, _ = await TestExs.update_or_create({"ok": ok}, ex=client.ex, action=ExAction.cur_pms_map)
            assert t.ok, "No pms for cur"
            logging.info(f"{client.ex.name}:{ExAction.pms.name} - ok")
