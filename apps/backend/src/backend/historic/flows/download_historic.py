from dotenv import load_dotenv

load_dotenv()

from prefect import flow
from backend.settings import settings
from backend.historic.tasks.sync_year import sync_year


@flow
def download_historic():
    for year in settings.HISTORIC_YEARS:
        sync_year(year=year)


if __name__ == "__main__":
    download_historic()
