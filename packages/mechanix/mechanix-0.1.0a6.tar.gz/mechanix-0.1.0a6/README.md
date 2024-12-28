# Mechanix Python API

[![PyPI version](https://img.shields.io/pypi/v/mechanix.svg)](https://pypi.org/project/mechanix/)

The Mechanix Python library provides convenient access to the Mechanix REST API from any Python 3.8+
application. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients.

## Documentation
- [General Documentation](https://docs.mechanix.tools)
- [REST API Reference](https://api.mechanix.tools/docs)
- [Python SDK API](api.md)

## Installation

```sh
pip install --pre mechanix
```

## Usage

```python
from mechanix import Mechanix

client = Mechanix()

response = client.tools.search_web(
    query="Common organelles within a human eukaryote",
)
print(response.request_id)
```

While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `MECHANIX_API_KEY="My API Key"` to your `.env` file
so that your API Key is not stored in source control.

## Async usage

Simply import `AsyncMechanix` instead of `Mechanix` and use `await` with each API call:

```python
import asyncio
from mechanix import AsyncMechanix

client = AsyncMechanix()


async def main() -> None:
    response = await client.tools.search_web(
        query="Common organelles within a human eukaryote",
    )
    print(response.request_id)


asyncio.run(main())
```

Functionality between the synchronous and asynchronous clients is otherwise identical.

## Handling errors

When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of `mechanix.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `mechanix.APIStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `mechanix.APIError`.

```python
import mechanix
from mechanix import Mechanix

client = Mechanix()

try:
    client.tools.search_web(
        query="Common organelles within a human eukaryote",
    )
except mechanix.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except mechanix.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except mechanix.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `APIConnectionError`       |





## Credits
This API library is generated with [Stainless](https://www.stainlessapi.com/).