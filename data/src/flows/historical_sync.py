from prefect import flow

@flow(
    name="Sync Historical TBA Data",
    description="Sync Historical FRC Data, including teams, events, matches, alliances, and rankings from The Blue Alliance (TBA) API.",

    log_prints=True,

    retries=1,
    retry_delay_seconds=10
)
def historical_sync():
    pass
