from asyncio import run

from x_model import init_db
from xync_client.Abc.Base import DictOfDicts, FlatDict
from xync_schema import models
from xync_schema.models import Ex

from xync_client.Abc.Ex import BaseExClient
from xync_client.BingX.base import BaseBingXClient
from xync_client.loader import PG_DSN


class ExClient(BaseExClient, BaseBingXClient):
    headers: dict[str, str] = {
        "app_version": "9.0.5",
        "device_id": "ccfb6d50-b63b-11ef-b31f-ef1f76f67c4e",
        "lang": "ru-RU",
        "platformid": "30",
    }

    # 20: Список всех платежных методов на бирже
    async def pms(self) -> DictOfDicts:  # {pm.exid: pm}
        curs = await self.curs()
        pp = {}
        for _id, cur in curs.items():
            pms = await self._get("/api/c2c/v1/advert/payment/list", params={"fiat": cur})
            [pp.update({p["id"]: {"name": p["name"], "logo": p["icon"]}}) for p in pms["data"]["paymentMethodList"]]
        return pp

    # 21: Список поддерживаемых валют
    async def curs(self) -> FlatDict:  # {cur.exid: cur.ticker}
        params = {
            "type": "1",
            "asset": "USDT",
            "coinType": "2",
        }
        curs = await self._get("/api/c2c/v1/common/supportCoins", params=params)
        return {cur["id"]: cur["name"] for cur in curs["data"]["coins"]}

    # 22: cur_pms_map
    async def cur_pms_map(self):
        pass

    # 23: coins
    async def coins(self):
        pass

    # 24: ads
    async def ads(self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None):
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="BingX")
    cl = ExClient(bg)
    await cl.pms()
    await cl.close()


if __name__ == "__main__":
    run(main())
