from x_client.http import Client as HttpClient
from xync_client.Abc.Auth import BaseAuthClient

from xync_client.TgWallet.pyro import PyroClient


class AuthClient(BaseAuthClient):
    async def _get_auth_hdrs(self) -> dict[str, str]:
        pyro = PyroClient(self.agent)
        init_data = await pyro.get_init_data()
        tokens = HttpClient("walletbot.me")._post("/api/v1/users/auth/", init_data)
        return {"Wallet-Authorization": tokens["jwt"], "Authorization": "Bearer " + tokens["value"]}
