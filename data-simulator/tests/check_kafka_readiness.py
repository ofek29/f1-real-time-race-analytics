import os
import time
from confluent_kafka.admin import AdminClient
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logger import logger

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


def check_kafka_ready(broker=bootstrap_servers, timeout=60):
    """
    Waits for Kafka broker to be ready by attempting to create a topic.

    :param broker: Kafka broker address.
    :param timeout: Time in seconds to wait before giving up.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            admin_client = AdminClient(
                {"bootstrap.servers": broker, "retries": 0, "log_level": 0}
            )

            cluster = admin_client.list_topics(timeout=5)
            if not cluster.brokers:
                raise Exception("No brokers found in cluster metadata.")
            return True
        except Exception as e:
            logger.error(f"Waiting for Kafka... {str(e)}")
            time.sleep(10)

    logger.error("Kafka did not start in time.")
    return False


if __name__ == "__main__":
    if check_kafka_ready():
        print("Proceeding with application startup...")
    else:
        exit(1)
