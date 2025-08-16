import os
from dataclasses import dataclass, field
from enum import StrEnum

import httpx
import polars as pl
from db_client import DBClient
from dotenv import load_dotenv


load_dotenv()


class _TBAEndpoint(StrEnum):
    STATUS = "/status"


@dataclass
class _TBAConfig:
    api_key: str = field(init=False)
    base_url: str = "https://www.thebluealliance.com/api/v3"
    slowdown: int = 1  # In Seconds
    timeout: int = 10  # In Seconds

    def __post_init__(self):
        env_api_key = os.getenv("TBA_API_KEY")

        if not env_api_key or not env_api_key.strip():
            raise ValueError("TBA API Key Not Found")

        if not isinstance(env_api_key, str):
            raise TypeError("TBA API Key Must Be A String")

        self.api_key = env_api_key


class TBAClient:
    def __init__(self, db_client: DBClient):
        self.config = _TBAConfig()
        self.db_client = db_client

    def _get(self, endpoint: _TBAEndpoint) -> dict | list | None:
        etag: str | None = self.db_client.get_etag(endpoint=endpoint.value)

        headers = {"X-TBA-Auth-Key": self.config.api_key}
        if etag is not None:
            headers["If-None-Match"] = etag

        req = httpx.get(
            url=self.config.base_url + endpoint.value,
            headers=headers,
            timeout=self.config.timeout,
        )

        if req.status_code == 304:
            return None

        req.raise_for_status()

        response_etag: str | None = req.headers.get("ETag")
        if response_etag is not None:
            self.db_client.set_etag(endpoint=endpoint, etag=response_etag)

        return req.json()

    def _get_as_df(self, endpoint: _TBAEndpoint) -> pl.DataFrame | None:
        res = self._get(endpoint=endpoint)

        if res is None:
            return None

        return pl.from_dicts(res)

    def get_status(self):
        return self._get(endpoint=_TBAEndpoint.STATUS)
