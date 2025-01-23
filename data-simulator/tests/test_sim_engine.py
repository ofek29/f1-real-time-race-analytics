import json
import time
import pytest
import os
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic
from simulator import DataSimulator

# Kafka Consumer Configuration
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
print(f"KAFKA_BOOTSTRAP_SERVERS: {bootstrap_servers}")
consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'test-consumer-group',
    'auto.offset.reset': 'earliest'
}

@pytest.fixture
def setup_kafka():
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
    topic_name = 'telemetry_row_data'

    # Check if the topic exists, otherwise create it
    existing_topics = admin_client.list_topics(timeout=10).topics
    if topic_name not in existing_topics:
        new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
        admin_client.create_topics([new_topic])
        print(f"Topic '{topic_name}' created.")
        time.sleep(2)  # Wait for the topic to become available
    else:
        print(f"Topic '{topic_name}' already exists.")
    yield


def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Consumer {consumer} subscribed to {p.topic}, partition {p.partition}')

@pytest.fixture
def kafka_consumer():
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['telemetry_row_data'], on_assign=assignment_callback)
    yield consumer
    consumer.close()


def test_data_simulator_integration(setup_kafka, kafka_consumer):
    num_cars = 3
    simulator = DataSimulator(num_cars)
    simulator.run()
    # Verify messages for each car
    for _ in range(num_cars):
        msg = kafka_consumer.poll(timeout=10.0)
        print(f"Received message: {msg.value()}")
        assert msg is not None, "No message received for car telemetry."
        assert not msg.error(), f"Consumer error: {msg.error()}"
        received_data = json.loads(msg.value().decode('utf-8'))
        assert "id" in received_data, "Received data missing 'id' field."
        assert "speed" in received_data, "Received data missing 'speed' field."
        assert "location" in received_data, "Received data missing 'location' field."