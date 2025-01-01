from prefect import task
from backend.historic.tasks.year.sync_matches import sync_matches
from backend.historic.tasks.year.sync_ranks import sync_ranks
from backend.historic.tasks.year.sync_teams import sync_teams
from backend.historic.tasks.year.sync_events import sync_events


@task(
    name="Historic Year Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_year(year: int):
    print(f"Syncing Year {year}")
    sync_teams(year=year)
    sync_events(year=year)
    sync_matches(year=year)
    sync_ranks(year=year)
