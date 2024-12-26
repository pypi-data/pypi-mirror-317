from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

# Configuration class for default settings
class NetworkConfig:
    DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
    DEFAULT_TIMEOUT = 30
    HANDLE_COOKIES = False
    IS_PRINTABLE = True


# Abstract Async Endpoint
class AsyncEndpoint(ABC):
    @property
    @abstractmethod
    def path(self) -> str:
        pass

    @property
    @abstractmethod
    def method(self) -> str:
        pass

    @property
    @abstractmethod
    def params(self) -> Optional[Dict[str, Any]]:
        pass

    @property
    @abstractmethod
    def headers(self) -> Optional[Dict[str, str]]:
        pass

    async def execute(self, client: "NetworkClient") -> Any: # by using quotes it becomes a forward reference, meaning until runtime when it is actually needed 
        from .client import NetworkClient  # Delayed import to avoid circular dependency
        """Execute the request using the provided NetworkClient."""
        if self.method == "GET":
            return await client.get(self.path, self.params, self.headers)
        elif self.method == "POST":
            return await client.post(self.path, self.params, self.headers)
        elif self.method == "PUT":
            return await client.put(self.path, self.params, self.headers)
        elif self.method == "DELETE":
            return await client.delete(self.path, self.params, self.headers)
        else:
            raise ValueError(f"Unsupported method: {self.method}")
