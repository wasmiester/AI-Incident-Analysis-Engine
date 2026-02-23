import time
from producer import emit_metric

SERVICE_NAME = "auth_service"

EMIT_INTERVAL_SECONDS = 5


def run():
    print(f"-- {SERVICE_NAME} started")

    while True:
        emit_metric()
        time.sleep(EMIT_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
