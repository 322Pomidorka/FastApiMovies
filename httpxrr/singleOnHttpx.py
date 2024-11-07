from typing import Optional, Any

import httpx

headers = {
        'X-API-KEY': 'd62320ea-2de1-4a35-8896-38b996ea8008'
    }

class Singletonhttpx:
    httpx_client: Optional[httpx.AsyncClient] = None

    @classmethod
    def get_httpx_client(cls) -> httpx.AsyncClient:
        if cls.httpx_client is None:
            timeout = httpx.Timeout(timeout=2)
            limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
            cls.httpx_client = httpx.AsyncClient(headers=headers, timeout=timeout, limits=limits)

        return cls.httpx_client

    @classmethod
    async def close_httpx_client(cls) -> None:
        if cls.httpx_client:
            await cls.httpx_client.close()
            cls.httpx_client = None

    @classmethod
    async def query_url(cls, url: str) -> Any:
        client = cls.get_httpx_client()

        try:
            response = await client.get(url)
            if response.status_code != 200:
                return {"ERROR OCCURED" + str(await response.text())}

            json_result = response.json()
        except Exception as e:
            return {"ERROR": e}

        return json_result


async def on_start_up() -> None:
    Singletonhttpx.get_httpx_client()


async def on_shutdown() -> None:
    await Singletonhttpx.close_httpx_client()

