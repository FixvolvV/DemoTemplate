import httpx


class HttpxClientManager:

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.AsyncClient:

        if self._client is None or self._client.is_closed:
            raise RuntimeError(
                "httpx client is not initialized. "
                "Make sure the application has started."
            )
        return self._client

    async def start(self) -> None:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(10.0, connect=5.0),
                limits=httpx.Limits(
                    max_connections=100,
                    max_keepalive_connections=20,
                ),
            )

    async def stop(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None


httpx_client_manager = HttpxClientManager()


async def get_httpx_client() -> httpx.AsyncClient:
    return httpx_client_manager.client
