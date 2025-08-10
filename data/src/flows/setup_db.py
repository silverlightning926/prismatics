from prefect import flow

from clients.db_client import DBClient

@flow(
    name="Setup Database Schema",
    description="Setup Full Database Schema Including Schemas And Tables. Does Not Handle Creating The Database, User Managment Or Other Items.",
    retries=2,
    retry_delay_seconds=5
)
def setup_db(DB_CLIENT: DBClient):
    DB_CLIENT.setup_database(drop_existing=True)
