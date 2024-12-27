from typing import Optional
from supabase import create_client, Client
from os import getenv
from backend.models.etag import Etag
from backend.models.tba.team import Team
from backend.models.sync_log import SyncLog

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
    supabase.table("etags").upsert(
        json=etag.model_dump(),
        on_conflict=["endpoint"],
    ).execute()


def save_teams(teams: list[Team]):
    supabase.table("teams").upsert(
        json=[team.model_dump() for team in teams],
        on_conflict=["key"],
    ).execute()


def save_snyc_log(
    sync_log: SyncLog,
):
    supabase.table("sync-logs").insert(
        json=sync_log.model_dump(),
    ).execute()
