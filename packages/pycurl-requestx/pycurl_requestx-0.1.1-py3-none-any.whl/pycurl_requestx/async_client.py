from pycurl_requests import *
import pycurl_requests as curl
import anyio

class AsyncClient:
    def __init__(self):
        self.client = curl.Session()
        self.TRACE = self.trace
        self.HEAD = self.head
        self.GET = self.get
        self.POST = self.post
        self.PUT = self.put
        self.PATCH = self.patch
        self.DELETE = self.delete

    async def request(self, method: str, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.request(method, url, **kwargs))
        return response

    async def trace(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.request('TRACE', url, **kwargs))
        return response

    async def head(self, url: str):
        response = await anyio.to_thread.run_sync(lambda: self.client.request('HEAD', url))
        return response

    async def get(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.get(url, **kwargs))
        return response

    async def post(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.post(url, **kwargs))
        return response

    async def put(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.put(url, **kwargs))
        return response

    async def patch(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.patch(url, **kwargs))
        return response

    async def delete(self, url: str, **kwargs):
        response = await anyio.to_thread.run_sync(lambda: self.client.delete(url, **kwargs))
        return response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self


asynchronous_client = AsyncClient()


async def request(method: str, url: str, **kwargs):
    return asynchronous_client.request(method, url, **kwargs)

async def trace(url: str, **kwargs):
    return asynchronous_client.request('TRACE', url, **kwargs)

async def head(url: str):
    return asynchronous_client.request('HEAD', url)

async def get(url: str, **kwargs):
    return asynchronous_client.get(url, **kwargs)

async def post(url: str, **kwargs):
    return asynchronous_client.post(url, **kwargs)

async def put(url: str, **kwargs):
    return asynchronous_client.put(url, **kwargs)

async def patch(url: str, **kwargs):
    return asynchronous_client.patch(url, **kwargs)

async def delete(url: str, **kwargs):
    return asynchronous_client.delete(url, **kwargs)


TRACE = trace
HEAD = head
GET = get
POST = post
PUT = put
PATCH = patch
DELETE = delete
