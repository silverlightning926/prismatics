from pprint import pprint
from typing import Optional
from supabase import create_client, Client
from os import getenv
from backend.models.etag import Etag
from backend.models.tba.event import Event
from backend.models.tba.match import Match
from backend.models.tba.ranking import Ranking
from backend.models.tba.team import Team

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_KEY")


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase: Client = get_client()


def get_etag(endpoint: str) -> Optional[Etag]:
    response = (
        supabase.table("etags").select("*").eq("endpoint", endpoint).limit(1).execute()
    )

    if len(response.data) == 0:
        return None

    return Etag(
        endpoint=response.data[0]["endpoint"],
        etag=response.data[0]["etag"],
    )


def save_etag(etag: Etag):
    if etag:
        supabase.table("etags").upsert(
            json=etag.model_dump(),
            on_conflict=["endpoint"],
        ).execute()


def save_teams(teams: list[Team]):
    if teams:
        supabase.table("teams").upsert(
            json=[team.model_dump() for team in teams],
            on_conflict=["key"],
        ).execute()


def save_events(events: list[Event]):
    new_districts = list(
        {
            event.district.key: event.district.model_dump()
            for event in events
            if event.district
        }.values()
    )

    if new_districts:
        supabase.table("event-districts").upsert(
            json=new_districts,
        ).execute()

    new_events = [event.model_dump() for event in events]

    for event in new_events:
        event.pop("webcasts")
        event.pop("division")
        if event.get("district"):
            event["district_key"] = event["district"]["key"]
        else:
            event["district_key"] = None
        event.pop("district")

    if new_events:
        supabase.table("events").upsert(
            json=new_events,
            on_conflict=["key"],
        ).execute()

    new_divisions = [event.division.model_dump() for event in events if event.division]
    if new_divisions:
        supabase.table("event-divisions").upsert(
            json=new_divisions,
        ).execute()

    webcasts = [webcast.model_dump() for event in events for webcast in event.webcasts]
    if webcasts:
        supabase.table("event-webcasts").upsert(
            json=webcasts,
        ).execute()


def get_event_keys_for_year(year: int) -> list[str]:
    response = (
        supabase.table("events")
        .select("key")
        .eq("year", year)
        .order("start_date")
        .execute()
    )
    return [event["key"] for event in response.data]


def upsert_matches(matches: list[Match]):
    new_matches = [
        match.model_dump(exclude={"alliances", "videos"}) for match in matches
    ]
    if new_matches:
        supabase.table("matches").upsert(json=new_matches).execute()

    new_alliances = [
        alliance.model_dump(exclude={"teams"})
        for match in matches
        for alliance in match.alliances
    ]
    if new_alliances:
        supabase.table("match-alliances").upsert(json=new_alliances).execute()

    new_alliance_teams = [
        alliance_team.model_dump(exclude={"teams"})
        for match in matches
        for alliance in match.alliances
        for alliance_team in alliance.teams
    ]
    if new_alliance_teams:
        supabase.table("alliance-teams").upsert(json=new_alliance_teams).execute()

    new_videos = [video.model_dump() for match in matches for video in match.videos]
    if new_videos:
        supabase.table("match-videos").upsert(json=new_videos).execute()


def upsert_ranks(ranks: list[Ranking]):
    new_rankings = [ranking.model_dump() for ranking in ranks]
    if new_rankings:
        supabase.table("rankings").upsert(json=new_rankings).execute()
