from prefect import task
from backend.services.tba_service import get_year_teams_page
from backend.services.db_service import save_teams
from time import sleep


@task
def sync_teams(year: int):
    page = 0
    while True:
        page_teams = get_year_teams_page(year=year, page=page)
        if not page_teams:
            break

        save_teams(page_teams)
        page += 1

        # TODO: Replace With Logging
        print(f"Synced {len(page_teams)} teams for {year} on page {page}")

        sleep(5.0)
