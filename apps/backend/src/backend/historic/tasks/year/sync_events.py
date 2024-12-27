from time import sleep
from prefect import task
from backend.services.db_service import save_events
from backend.utils.filter_utils import filter_events

from backend.services.tba_service import get_year_events
from backend.settings import settings


@task(
    name="Historic Event Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_events(year: int):
    events = get_year_events(year=year)
    events = filter_events(events)

    save_events(events)

    print(f"Event Sync ({year}) | Synced {len(events)} Events")

    sleep(settings.request_throttle_secs)
