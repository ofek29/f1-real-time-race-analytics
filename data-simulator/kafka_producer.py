import os
from logger import logger
from confluent_kafka import Producer
from tests.check_kafka_readiness import check_kafka_ready


# Configuration for the Kafka producer
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
config = {"bootstrap.servers": bootstrap_servers}

# Create Producer instance
try:
    if not check_kafka_ready():
        raise Exception("Kafka is not available")
    producer = Producer(config)
    logger.info("Producer instance created")
except Exception as e:
    logger.error(f"Failed to create producer: {e}")
    exit(1)


# Delivery callback for produced messages
def delivery_callback(err, msg):
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


# Produce some messages
def send_telemetry_data(car_data: str, topic="telemetry_row_data") -> bool:
    producer.produce(topic=topic, value=car_data, on_delivery=delivery_callback)
    producer.poll(0)
    producer.flush()
    return True
