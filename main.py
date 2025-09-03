from views.main_group import cli_main
from db.db_init import recreate_initial_db
import sentry_sdk

def main():
    # sentry_sdk.init(
    #     dsn="https://dbd1a94390867451a892d62027b03c80@o4509950155489280.ingest.de.sentry.io/4509950157389904",
    #     # Add data like request headers and IP for users,
    #     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    #     send_default_pii=True,
    # )
    cli_main()

if __name__ == "__main__":
    main()
