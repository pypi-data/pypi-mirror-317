import httpx
from typing import Any, Dict, Optional, Type
from .logger import logger
from .exceptions import (
    NetworkError,
    ConnectionError,
    TimeoutError,
    AuthenticationError,
    RateLimitExceeded,
)
from .endpoint import AsyncEndpoint, NetworkConfig

# Network Client
class NetworkClient:
    def __init__(self, base_url: str, config: Type[NetworkConfig] = NetworkConfig):
        self.base_url = base_url
        self.client = None
        self.config = config

    async def setup(self):
        """Set up the HTTP client."""
        self.client = httpx.AsyncClient(
            timeout=self.config.DEFAULT_TIMEOUT, follow_redirects=False
        )
        logger.info("NetworkClient setup completed.")

    async def get_default_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = self.config.DEFAULT_HEADERS.copy()
        if additional_headers:
            headers.update(additional_headers)
        return headers

    async def get_default_params(self, custom_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = {}
        if custom_params:
            params.update(custom_params)
        return params

    async def request(self, method: str, path: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        if not self.client:
            await self.setup()

        url = f"{self.base_url}/{path.lstrip('/')}"
        params = await self.get_default_params(params)
        headers = await self.get_default_headers(headers)

        try:
            response = await self.client.request(method, url, params=params, headers=headers)
            response.raise_for_status()
            if self.config.IS_PRINTABLE:
                logger.info(f"Response: {response.json()}")
            return response
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Authentication error", method=method, url=url, status_code=e.response.status_code)
                raise AuthenticationError() from e
            elif e.response.status_code == 403:
                logger.error("Rate limit exceeded", method=method, url=url, status_code=e.response.status_code)
                raise RateLimitExceeded() from e
            else:
                logger.error("HTTP status error", method=method, url=url, status_code=e.response.status_code)
                raise NetworkError() from e
        except httpx.ConnectTimeout as e:
            logger.error("Connection timeout error", method=method, url=url, detail=str(e))
            raise TimeoutError() from e
        except httpx.RequestError as e:
            logger.error("Request error", method=method, url=url, detail=str(e))
            raise ConnectionError() from e
        except Exception as e:
            logger.error("Unexpected error", method=method, url=url, detail=str(e))
            raise NetworkError() from e

    async def get(self, path: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        return await self.request("GET", path, params, headers)

    async def post(self, path: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> httpx.Response:
        return await self.request("POST", path, data, headers)

    async def put(self, path: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> httpx.Response:
        return await self.request("PUT", path, data, headers)

    async def delete(self, path: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> httpx.Response:
        return await self.request("DELETE", path, params, headers)

    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
            logger.info("NetworkClient connection closed.")
