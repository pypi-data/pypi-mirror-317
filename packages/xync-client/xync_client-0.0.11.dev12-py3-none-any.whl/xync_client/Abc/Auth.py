import logging
from abc import abstractmethod

from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from xync_schema.models import Agent

from xync_client.Abc.Base import BaseClient


class BaseAuthClient(BaseClient):
    def __init__(self, agent: Agent):
        self.headers.update(agent.auth)
        self.agent = agent
        self.meth = {
            "GET": self._get,
            "POST": self._post,
            "DELETE": self._delete,
        }
        super().__init__(agent.ex)

    @abstractmethod
    async def _get_auth_hdrs(self) -> dict[str, str]: ...

    async def login(self) -> None:
        auth_hdrs: dict[str, str] = await self._get_auth_hdrs()
        self.session.headers.update(auth_hdrs)

    async def _proc(self, resp: ClientResponse, data: dict = None) -> dict | str:
        try:
            return await super()._proc(resp)
        except HttpProcessingError as e:
            if e.code == 401:
                logging.warning(e)
                await self.login()
                res = await self.meth[resp.method](resp.url.path, data)
                return res
