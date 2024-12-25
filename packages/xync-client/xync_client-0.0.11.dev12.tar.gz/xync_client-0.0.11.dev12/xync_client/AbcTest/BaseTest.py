import pytest
from typing import TypeGuard
from src.loader import PG_DSN
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from xync_schema import models
from xync_schema.models import Ex

from xync_client.Abc.Base import DictOfDicts, ListOfDicts, FlatDict, MapOfIdsList, BaseClient


class BaseTest:
    def __init__(self, ex_name: str):
        self.exq = Ex.get(name=ex_name)

    @pytest.fixture(scope="class", autouse=True)
    async def cn(self) -> AsyncpgDBClient:
        cn: AsyncpgDBClient = await init_db(PG_DSN, models, True)
        yield cn
        await cn.close()

    @pytest.fixture(scope="class", autouse=True)
    async def cl(self) -> BaseClient:
        bcl = BaseClient(await self.exq)
        yield bcl
        await bcl.close()

    @staticmethod
    def is_dict_of_dicts(dct: DictOfDicts) -> TypeGuard[DictOfDicts]:
        return all(isinstance(k, int | str) and isinstance(v, dict) for k, v in dct.items())

    @staticmethod
    def is_list_of_dicts(lst: ListOfDicts) -> TypeGuard[ListOfDicts]:
        return all(isinstance(el, dict) for el in lst)

    @staticmethod
    def is_flat_dict(dct: FlatDict) -> TypeGuard[FlatDict]:
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())

    @staticmethod
    def is_map_of_ids(dct: MapOfIdsList) -> TypeGuard[MapOfIdsList]:
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())
