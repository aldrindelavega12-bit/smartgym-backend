import requests
import time

from sync.user_account_sync import sync_user_accounts
from sync.cloud_sync import sync_pending_members
from sync.trainer_sync import sync_trainer_plans


def start_cloud_worker():

    print("[CLOUD] Worker Started")

    while True:

        try:

            # Sync accounts first
            sync_user_accounts()
            
            # Sync trainer plans
            sync_trainer_plans()

            # Then sync pending registrations
            sync_pending_members()

        except requests.exceptions.RequestException:

            print("[CLOUD] Cloud API unavailable.")

        except Exception as e:

            print(f"[CLOUD] {e}")

        time.sleep(5)