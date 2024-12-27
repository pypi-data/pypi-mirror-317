import httpx

from ..taptypes import Bot, BotRequest


class AsyncTapSageUser:
    API_V1 = "https://api.tapsage.com/api/v1"

    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoints = {
            "bots": f"{self.API_V1}/bots",
            "get_bot": f"{self.API_V1}/bots/{{bot_id}}",
        }
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
        self._session = None

    async def get_session(self):
        if self._session is None:
            self._session = httpx.AsyncClient()
        return self._session

    async def _request(self, method: str, endpoint: str, **kwargs):
        url = self.endpoints.get(endpoint).format(**kwargs.get("url_params", {}))
        async with httpx.AsyncClient() as session:
            response = await session.request(
                method, url, headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def create_bot(self, bot_data: BotRequest):
        assert isinstance(bot_data, BotRequest)
        response_data = await self._request(
            method="POST", endpoint="bots", json=bot_data.model_dump()
        )
        return Bot(**response_data)

    async def retrieve_bot(self, bot_id: str):
        response_data = await self._request(
            method="GET", endpoint="get_bot", url_params={"bot_id": bot_id}
        )
        return response_data

    async def close(self):
        if self._session is not None:
            await self._session.close()
            self._session = None
