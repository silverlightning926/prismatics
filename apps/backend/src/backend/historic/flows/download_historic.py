from prefect import flow
from settings import settings
from tasks.sync_year import sync_year


@flow
def download_historic():
    for year in settings.HISTORIC_YEARS:
        sync_year(year=year)


if __name__ == "__main__":
    download_historic()
