from prefect import task


@task
def sync_teams(year: int):
    print(f"Syncing teams for {year}")
