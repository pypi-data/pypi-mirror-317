# Network Layer Library

The **Network Layer Library** is a Python package designed to provide a structured, reusable, and extensible way to handle HTTP requests and responses. Built on top of the powerful [`httpx`](https://www.python-httpx.org/) library, it enables efficient and modern asynchronous HTTP communication.

---

## Features

- **Async Support**: Fully asynchronous client for high-performance HTTP operations using `httpx`.
- **Configurable Endpoints**: Easily define and reuse endpoints with custom headers, parameters, and HTTP methods.
- **Centralized Logging**: Built-in structured logging for requests and responses using `structlog`.
- **Error Handling**: Comprehensive error management for authentication, rate limiting, timeouts, and other issues.
- **Flexible Configuration**: Customize headers, timeouts, and cookie handling.
- **Poetry & Pip Friendly**: Designed to work seamlessly with `poetry` for managing dependencies and publishing, while remaining compatible with `pip` for installation.

---

## Installation

### Install from PyPI
You can install the package using `pip`:

```bash
pip install network-layer
```

### Install Locally Using Poetry
If you are using `poetry` for dependency management:

```bash
poetry add network-layer
```

---

## Usage

### Setting Up the Client
```python
from network_layer import NetworkClient

# Initialize the client
client = NetworkClient(base_url="https://example.com")
await client.setup()
```

### Creating Custom Endpoints
```python
from network_layer import AsyncEndpoint
from typing import Optional, Dict, Any

class MyCustomEndpoint(AsyncEndpoint):
    @property
    def path(self) -> str:
        return "api/v1/resource"

    @property
    def method(self) -> str:
        return "GET"

    @property
    def params(self) -> Optional[Dict[str, Any]]:
        return {"key": "value"}

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        return {"Authorization": "Bearer token"}
```

### Making a Request
```python
endpoint = MyCustomEndpoint()
response = await endpoint.execute(client)
print(response.json())
await client.close()
```

---

## Development

### Running Tests
Tests are located in the `tests/` directory. Use `pytest` to run them:

```bash
pytest
```

### Building the Package
To build the package for distribution:

```bash
poetry build
```

### Publishing to PyPI
Make sure you’re logged into PyPI via Poetry:

```bash
poetry config pypi-token.pypi <your-token>
poetry publish --build
```

---

## Why Use This Library?

1. **Built on `httpx`:** Leveraging the power and simplicity of the `httpx` library, this package adds structure and extensibility for advanced use cases.
2. **Poetry-Compatible:** Designed to work seamlessly with `poetry`, enabling easier dependency management and publishing workflows, while remaining fully compatible with `pip`.
3. **Asynchronous by Design:** Supports high-performance asynchronous programming for modern Python applications.

---
## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Contributing

Contributions are welcomed! Please fork the repository and submit a pull request.

---