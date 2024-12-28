from abc import abstractmethod
from asyncio import AbstractEventLoop
from typing import TypeGuard

import pytest
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from xync_client.Abc.Base import BaseClient, DictOfDicts, ListOfDicts, FlatDict, MapOfIdsList
from xync_schema import models

from xync_client.loader import PG_DSN


class BaseTest:
    loop: AbstractEventLoop

    # @pytest.fixture(scope="class", autouse=True)
    # def event_loop_policy(self):
    #     return uvloop.EventLoopPolicy()

    @pytest.fixture(scope="class", autouse=True)
    async def cn(self) -> AsyncpgDBClient:
        cn: AsyncpgDBClient = await init_db(PG_DSN, models, True)
        yield cn
        await cn.close()

    @abstractmethod
    @pytest.fixture(scope="class")
    async def clients(self) -> list[BaseClient]: ...

    @staticmethod
    def is_dict_of_dicts(dct: DictOfDicts, not_empty: bool = True) -> TypeGuard[DictOfDicts]:
        if not_empty and not len(dct):
            return False
        return all(isinstance(k, int | str) and isinstance(v, dict) for k, v in dct.items())

    @staticmethod
    def is_list_of_dicts(lst: ListOfDicts, not_empty: bool = True) -> TypeGuard[ListOfDicts]:
        if not_empty and not len(lst):
            return False
        return all(isinstance(el, dict) for el in lst)

    @staticmethod
    def is_flat_dict(dct: FlatDict, not_empty: bool = True) -> TypeGuard[FlatDict]:
        if not_empty and not len(dct):
            return False
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())

    @staticmethod
    def is_map_of_ids(dct: MapOfIdsList, not_empty: bool = True) -> TypeGuard[MapOfIdsList]:
        if not_empty and not len(dct):
            return False
        return all(isinstance(k, int | str) and isinstance(v, str) for k, v in dct.items())
