
import time
import logging

from sync.sync_maintenance import sync_all_maintenance


SYNC_INTERVAL = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def run_service():

    logging.info("Maintenance Sync Service Started")

    while True:

        try:
            sync_all_maintenance()

        except Exception:
            logging.exception("Maintenance sync error")

        time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    run_service()
