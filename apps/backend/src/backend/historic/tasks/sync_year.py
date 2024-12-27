from prefect import task
from backend.historic.tasks.year.sync_teams import sync_teams


@task(
    name="Historic Year Sync",
    tags=["historic"],
    retries=3,
    retry_delay_seconds=15,
    log_prints=True,
)
def sync_year(year: int):
    sync_teams(year=year)
