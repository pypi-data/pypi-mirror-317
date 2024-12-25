from aiohttp import ClientSession, ClientResponse
from aiohttp.http_exceptions import HttpProcessingError

from x_client import HttpNotFound, df_hdrs


class Client:
    host: str | None  # required
    headers: dict[str, str] = df_hdrs
    cookies: dict[str, str] = None
    session: ClientSession

    def __init__(self, host: str = None):
        base_url = f"https://{h}" if (h := host or self.host) else h
        self.session = ClientSession(base_url, headers=self.headers, cookies=self.cookies)

    async def close(self):
        await self.session.close()

    # noinspection PyMethodMayBeStatic
    def _prehook(self, _payload: dict = None):
        return {}

    async def _get(self, url: str, params: dict = None):
        resp: ClientResponse = await self.session.get(url, params=params, headers=self._prehook(params))
        return await self._proc(resp)

    async def _post(self, url: str, data: dict = None):
        dt = {"json" if isinstance(data, dict) else "data": data}
        resp = await self.session.post(url, **dt, headers=self._prehook(data))
        return await self._proc(resp)

    async def _delete(self, url: str, params: dict = None):
        resp: ClientResponse = await self.session.delete(url, params=params, headers=self._prehook(params))
        return await self._proc(resp)

    async def _proc(self, resp: ClientResponse, data=None) -> dict | str:
        if not str(resp.status).startswith("2"):
            if resp.status == 404:
                raise HttpNotFound()
            raise HttpProcessingError(code=resp.status, message=await resp.text())
        if resp.content_type.endswith("/json"):
            return await resp.json()
        return await resp.text()
