from time import sleep
from prefect import task
from backend.settings import settings
from backend.services.db_service import (
    get_event_keys_for_year,
    save_etag,
)
from backend.services.tba_service import get_event_rankings
from backend.services.db_service import upsert_ranks


@task(
    name="Historic Rank Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_ranks(year: int):
    event_keys = get_event_keys_for_year(year=year)

    for event_key in event_keys:
        result = get_event_rankings(event_key=event_key)

        if not result:
            print(f"Rank Sync ({event_key}) | ETag Match")
            sleep(settings.request_throttle_secs)
            continue

        ranks, etag = result

        upsert_ranks(ranks=ranks)

        save_etag(etag)

        print(f"Rank Sync ({event_key}) | Synced {len(ranks)} Ranks")

        sleep(settings.request_throttle_secs)
