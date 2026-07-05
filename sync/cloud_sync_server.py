from sync.cloud_worker import start_cloud_worker


def start_server():

    print("[CLOUD] Cloud Sync Server Started")

    start_cloud_worker()


if __name__ == "__main__":

    start_server()