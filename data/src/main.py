from dotenv import load_dotenv
load_dotenv()

from flows.historical_sync import historical_sync

def main():
    historical_sync()

    historical_sync.serve(
        name="Sync Historical TBA Data",
        cron="0 2 * * 2,5",
    )

if __name__ == "__main__":
    main()
