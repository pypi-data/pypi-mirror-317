import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import aiohttp
import asyncio

# SyncRetryClient for synchronous requests
class SyncRetryClient:
    def __init__(self, retries=3, backoff_factor=1, status_forcelist=None):
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist or [429, 500, 502, 503, 504]
        self.session = self._create_session()

    def _create_session(self):
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=["GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.post(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data=data, **kwargs)
    def patch(self, url, data=None, **kwargs):
        return self.session.patch(url, data=data, **kwargs)
    

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)


# AsyncRetryClient for asynchronous requests
class AsyncRetryClient:
    def __init__(self, retries=3, delay=2, status_forcelist=None):
        self.retries = retries
        self.delay = delay
        self.status_forcelist = status_forcelist or [429, 500, 502, 503, 504]

    async def _fetch(self, session, url, method="GET", **kwargs):
        for attempt in range(1, self.retries + 1):
            try:
                if method.upper() == "GET":
                    async with session.get(url, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "POST":
                    async with session.post(url, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "PUT":
                    async with session.put(url, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "DELETE":
                    async with session.delete(url, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
                elif method.upper() == "PATCH":
                    async with session.patch(url, **kwargs) as response:
                        if response.status not in self.status_forcelist:
                            return await response.text()
                        print(f"Attempt {attempt}: Status {response.status}")
            except aiohttp.ClientError as e:
                print(f"Attempt {attempt}: Error - {e}")

            if attempt < self.retries:
                await asyncio.sleep(self.delay)

        raise Exception("All retry attempts failed")

    async def get(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="GET", **kwargs)

    async def post(self, url, data=None, json=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="POST", data=data, json=json, **kwargs)

    async def put(self, url, data=None, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="PUT", data=data, **kwargs)

    async def delete(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="DELETE", **kwargs)
    
    async def patch(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            return await self._fetch(session, url, method="PATCH", **kwargs)