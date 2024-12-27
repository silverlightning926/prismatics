from typing import Optional

from backend.models.etag import Etag
from backend.models.sync_log import SyncLog
from backend.models.tba.team import Team
from backend.services.db_service import get_etag, save_etag, save_snyc_log

import requests
from os import getenv

BASE_URL = "https://www.thebluealliance.com/api/v3"
HEADERS = {
    "X-TBA-Auth-Key": getenv("TBA_API_KEY"),
}


def get_year_teams_page(
    year: int,
    page: int,
) -> list[Team]:

    endpoint = f"/teams/{year}/{page}"
    etag = get_etag(endpoint)

    if etag:
        HEADERS["If-None-Match"] = etag.etag

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
    )

    save_snyc_log(SyncLog(endpoint=endpoint, status_code=response.status_code))

    if response.status_code == 304:
        return []

    response.raise_for_status()

    save_etag(Etag(endpoint=endpoint, etag=response.headers["ETag"]))

    return [Team.from_dict(team) for team in response.json()]