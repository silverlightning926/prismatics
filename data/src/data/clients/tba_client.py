from dotenv import load_dotenv
load_dotenv()

from enum import StrEnum
from dataclasses import dataclass, field
import os
import httpx
import polars as pl

@dataclass
class TBAJsonResponse:
    data: dict | list | None
    etag: str | None

@dataclass
class TBADataFrameResponse:
    data: pl.DataFrame | None
    etag: str | None

class _TBAEndpoint(StrEnum):
    STATUS = "/status"

@dataclass
class _TBAConfig():
    api_key: str = field(init=False)
    base_url: str = "https://www.thebluealliance.com/api/v3"
    slowdown: int = 1 # In Seconds
    timeout: int = 10 # In Seconds

    def __post_init__(self):
        env_key = os.getenv("TBA_API_KEY")

        if not env_key or not env_key.strip():
            raise ValueError("TBA API Key Not Found")

        if not isinstance(env_key, str):
            raise TypeError("TBA API Key Must Be A String")

        self.api_key = env_key

class TBAClient:
    def __init__(self):
        self.config = _TBAConfig()

    def _get(self, endpoint: _TBAEndpoint, etag: str | None = None) -> TBAJsonResponse:
        headers = {'X-TBA-Auth-Key': self.config.api_key}
        if etag is not None:
            headers['If-None-Match'] = etag

        req = httpx.get(
            url=self.config.base_url + endpoint.value,
            headers=headers,
            timeout=self.config.timeout
        )

        response_etag = req.headers.get('ETag')

        if req.status_code == 304:
            return TBAJsonResponse(data=None, etag=response_etag)

        req.raise_for_status()

        return TBAJsonResponse(
            data=req.json(),
            etag=response_etag
        )

    def _get_as_df(self, endpoint: _TBAEndpoint, etag: str | None = None) -> TBADataFrameResponse:
        res: TBAJsonResponse = self._get(endpoint=endpoint, etag=etag)

        if res.data is None:
            return TBADataFrameResponse(data=None, etag=res.etag)

        return TBADataFrameResponse(
            data=pl.from_dicts(res.data),
            etag=res.etag
        )

    def get_status(self, etag: str | None = None) -> TBAJsonResponse:
        return self._get(
            endpoint=_TBAEndpoint.STATUS,
            etag=etag
        )
