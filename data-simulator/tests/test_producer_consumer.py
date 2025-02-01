import json
import time
import pytest
import os
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from kafka_producer import send_telemetry_data

# Kafka Consumer Configuration
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
consumer_conf = {
    "bootstrap.servers": bootstrap_servers,
    "group.id": "test-consumer-group",
    "auto.offset.reset": "earliest",
}


@pytest.fixture(scope="module")
def kafka_admin_client():
    client = AdminClient({"bootstrap.servers": bootstrap_servers})
    yield client


@pytest.fixture
def setup_kafka(kafka_admin_client):
    topic_name = "telemetry_manual_test"

    # Check if the topic exists, otherwise create it
    existing_topics = kafka_admin_client.list_topics(timeout=10).topics
    if topic_name not in existing_topics:
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        kafka_admin_client.create_topics([new_topic])
        print(f"Topic '{topic_name}' created.")
    else:
        print(f"Topic '{topic_name}' already exists.")
    yield


def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f"Consumer {consumer} subscribed to {p.topic}, partition {p.partition}")


@pytest.fixture
def kafka_consumer():
    consumer = Consumer(consumer_conf)
    consumer.subscribe(["telemetry_manual_test"], on_assign=assignment_callback)
    yield consumer
    consumer.close()


def test_kafka_producer_consumer_integration(setup_kafka, kafka_consumer):
    # Test data
    test_data = json.dumps({"id": 1, "speed": 120, "location": 53})
    # Produce the message
    success = send_telemetry_data(test_data, "telemetry_manual_test")
    assert success, "Failed to send telemetry data with producer."

    # Poll the consumer to verify the message was sent
    msg = kafka_consumer.poll(timeout=10.0)
    print(f"Received message: {msg.value()}")
    assert msg is not None, "No message received from Kafka."
    assert not msg.error(), f"Consumer error: {msg.error()}"
    received_data = json.loads(msg.value().decode("utf-8"))
    assert received_data == json.loads(
        test_data
    ), "Received data does not match sent data."
