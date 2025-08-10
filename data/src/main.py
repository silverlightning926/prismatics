from dotenv import load_dotenv
load_dotenv()

from clients.db_client import DBClient

from flows.setup_db import setup_db
from flows.historical_sync import historical_sync

def main():
    DB_CLIENT: DBClient = DBClient()
    setup_db(DB_CLIENT=DB_CLIENT)

    historical_sync()

    historical_sync.serve(
        name="Sync Historical TBA Data",
        cron="0 2 * * 2,5",
    )

if __name__ == "__main__":
    main()
