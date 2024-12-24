import httpx

class ClientMixin:
  async def __aenter__(self):
    self._client = httpx.AsyncClient()
    return self
  
  async def __aexit__(self, *args):
    if self._client is not None:
      await self._client.aclose()
      self._client = None

  @property
  def client(self) -> httpx.AsyncClient:
    client = getattr(self, '_client', None)
    if client is None:
      raise RuntimeError('Please use as context manager: `async with ...: ...`')
    return client
