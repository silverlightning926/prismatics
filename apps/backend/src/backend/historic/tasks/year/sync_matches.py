from time import sleep
from prefect import task
from backend.settings import settings
from backend.services.db_service import (
    get_event_keys_for_year,
    save_etag,
    upsert_matches,
)
from backend.services.tba_service import get_event_matches


@task(
    name="Historic Match Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_matches(year: int):
    event_keys = get_event_keys_for_year(year=year)

    for event_key in event_keys:
        matches, etag = get_event_matches(event_key=event_key)

        upsert_matches(matches=matches)

        save_etag(etag)

        print(f"Match Sync ({event_key}) | Synced {len(matches)} Matches")

        sleep(settings.request_throttle_secs)
