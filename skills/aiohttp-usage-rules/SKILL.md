---
name: aiohttp-usage-rules
description: Enforce acceptable aiohttp usage patterns in Python async code. Use when adding or reviewing HTTP requests with aiohttp, especially for converting sync call paths to async, constructing ClientSession with timeout and headers, handling redirects with allow_redirects=False, and writing safe GET/POST request flows.
---

# aiohttp Usage Rules

## Convert call paths to async

- Make the function `async def` if it performs `aiohttp` I/O.
- Add `await` at every call site up the stack until the async boundary is reached.
- Do not call `aiohttp` request methods from synchronous functions.

```python
async def fetch_page(self, url: str) -> str:
  timeout = self._build_aiohttp_timeout()
  async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
    async with session.get(url, allow_redirects=False) as resp:
      return await resp.text()
```

## Build timeout and session once per request flow

Use the same pattern as `WebCache._request_with_redirects`:

```python
def _build_aiohttp_timeout(self) -> aiohttp.ClientTimeout:
  return aiohttp.ClientTimeout(sock_connect=6.05, sock_read=27)

async def request_with_redirects(self, url: str) -> tuple[int, bytes, dict[str, str]]:
  current_url = url
  max_redirects = 3
  timeout = self._build_aiohttp_timeout()

  async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
    for attempt in range(max_redirects):
      async with session.get(current_url, allow_redirects=False) as resp:
        status_code = resp.status
        headers = {k: v for k, v in resp.headers.items()}

        if 300 <= status_code < 400 and "Location" in headers:
          current_url = headers["Location"]
          if attempt < max_redirects - 1:
            continue

        body = await resp.read()
        return status_code, body, headers

  raise RuntimeError("Redirect handling exhausted without response")
```

## GET pattern

```python
async def get_json(self, current_url: str) -> dict:
  timeout = self._build_aiohttp_timeout()
  async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
    async with session.get(current_url, allow_redirects=False) as resp:
      resp.raise_for_status()
      return await resp.json()
```

## POST pattern

```python
async def post_json(self, current_url: str, payload: dict) -> dict:
  timeout = self._build_aiohttp_timeout()
  async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
    async with session.post(current_url, json=payload, allow_redirects=False) as resp:
      resp.raise_for_status()
      return await resp.json()
```

## Header example

Pass headers when creating the session, for example `User-Agent`, auth, and content type.

```python
self.headers = {
    "User-Agent": "recruiter-api/1.0",
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

timeout = self._build_aiohttp_timeout()
async with aiohttp.ClientSession(headers=self.headers, timeout=timeout) as session:
  async with session.get(url, allow_redirects=False) as resp:
    data = await resp.text()
```
