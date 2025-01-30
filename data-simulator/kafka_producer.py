import os
from confluent_kafka import Producer

# Configuration for the Kafka producer
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
config = {"bootstrap.servers": bootstrap_servers}

# Create Producer instance
producer = Producer(config)
print("Producer instance created.")


# Delivery callback for produced messages
def delivery_callback(err, msg):
    if err:
        print(f"Message failed delivery: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


# Produce some messages
def send_telemetry_data(car_data: str, topic="telemetry_row_data") -> bool:
    producer.produce(topic=topic, value=car_data, on_delivery=delivery_callback)
    producer.poll(0)
    producer.flush()
    return True
