from prefect import task
from backend.historic.tasks.year.sync_teams import sync_teams


@task
def sync_year(year: int):
    sync_teams(year=year)
