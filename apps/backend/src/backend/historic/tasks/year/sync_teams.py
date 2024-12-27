from prefect import task
from backend.services.tba_service import get_year_teams_page
from backend.services.db_service import save_teams
from time import sleep
from backend.settings import settings


@task(
    name="Historic Team Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_teams(year: int):
    page = 0
    while True:
        page_teams = get_year_teams_page(year=year, page=page)
        if not page_teams:
            break

        save_teams(page_teams)

        # TODO: Replace With Logging
        print(f"Team Sync ({year}) - Page {page}) | Synced {len(page_teams)} Teams")

        sleep(settings.request_throttle_secs)

        page += 1
