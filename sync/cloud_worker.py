import requests
import time
from sync.cloud_sync import sync_pending_members

def start_cloud_worker():

    print("[CLOUD] Worker Started")

    while True:

        try:

            sync_pending_members()

        except requests.exceptions.RequestException:

            print("[CLOUD] Cloud API unavailable.")

        except Exception as e:

            print(f"[CLOUD] {e}")

        time.sleep(5)