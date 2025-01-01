from backend.models.etag import Etag
from backend.models.tba.ranking import Ranking
from backend.models.tba.team import Team
from backend.models.tba.event import Event
from backend.models.tba.match import Match
from backend.services.db_service import get_etag

import requests
from os import getenv

BASE_URL = "https://www.thebluealliance.com/api/v3"
HEADERS = {
    "X-TBA-Auth-Key": getenv("TBA_API_KEY"),
}


def get_year_teams_page(
    year: int,
    page: int,
) -> tuple[list[Team], Etag]:

    endpoint = f"/teams/{year}/{page}"
    etag = get_etag(endpoint)

    if etag:
        HEADERS["If-None-Match"] = etag.etag

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
    )

    # ! TODO: Fix Bug - If 304 is returned, and empty list is returned then task will break before completing all pages
    if response.status_code == 304:
        return []

    response.raise_for_status()

    new_etag = Etag(endpoint=endpoint, etag=response.headers["ETag"])

    return [Team.from_dict(team) for team in response.json()], new_etag


def get_year_events(
    year: int,
) -> tuple[list[Event], Etag]:

    endpoint = f"/events/{year}"
    etag = get_etag(endpoint)

    if etag:
        HEADERS["If-None-Match"] = etag.etag

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
    )

    if response.status_code == 304:
        return []

    response.raise_for_status()

    new_etag = Etag(endpoint=endpoint, etag=response.headers["ETag"])

    return [Event.from_dict(event) for event in response.json()], new_etag


def get_event_matches(
    event_key: str,
) -> tuple[list[Match], Etag]:

    endpoint = f"/event/{event_key}/matches"
    etag = get_etag(endpoint)

    if etag:
        HEADERS["If-None-Match"] = etag.etag

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
    )

    if response.status_code == 304:
        return []

    response.raise_for_status()

    new_etag = Etag(endpoint=endpoint, etag=response.headers["ETag"])

    return [Match.from_dict(match) for match in response.json()], new_etag


def get_event_rankings(
    event_key: str,
) -> tuple[list[Ranking], Etag]:

    endpoint = f"/event/{event_key}/rankings"
    etag = get_etag(endpoint)

    if etag:
        HEADERS["If-None-Match"] = etag.etag

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=HEADERS,
    )

    if response.status_code == 304:
        return []

    response.raise_for_status()

    new_etag = Etag(endpoint=endpoint, etag=response.headers["ETag"])

    if not response.json()["rankings"]:
        return [], new_etag

    return [
        Ranking.from_dict(rank, event_key) for rank in response.json()["rankings"]
    ], new_etag
