import json
import pytest
from confluent_kafka import Consumer
from kafka_producer import send_telemetry_data
from simulator import DataSimulator
import os

# Kafka Consumer Configuration
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
print(f"KAFKA_BOOTSTRAP_SERVERS: {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}")
consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'test-consumer-group',
    'auto.offset.reset': 'earliest'
}

def assignment_callback(consumer, partitions):
    for p in partitions:
        print(f'Assigned to {p.topic}, partition {p.partition}, offset {p.offset}')

@pytest.fixture(scope="module")
def kafka_consumer():
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['telemetry_row_data'], on_assign=assignment_callback)
    yield consumer
    consumer.close()
        
def test_kafka_producer_consumer_integration(kafka_consumer):
    # Test data
    test_data = json.dumps({
        "id": 1,
        "speed": 120,
        "location": 53
    })

    # Produce the message
    success = send_telemetry_data(test_data)
    assert success, "Failed to send telemetry data with producer."

    # Poll the consumer to verify the message was sent
    msg = kafka_consumer.poll(timeout=10.0)

    assert msg is not None, "No message received from Kafka."
    assert not msg.error(), f"Consumer error: {msg.error()}"
    received_data = json.loads(msg.value().decode('utf-8'))
    assert received_data == json.loads(test_data), "Received data does not match sent data."

def test_data_simulator_integration(kafka_consumer):
    num_cars = 3
    simulator = DataSimulator(num_cars)

    simulator.run()

    # Verify messages for each car
    for _ in range(num_cars):
        msg = kafka_consumer.poll(timeout=10.0)
        assert msg is not None, "No message received for car telemetry."
        assert not msg.error(), f"Consumer error: {msg.error()}"

        received_data = json.loads(msg.value().decode('utf-8'))
        assert "id" in received_data, "Received data missing 'id' field."
        assert "speed" in received_data, "Received data missing 'speed' field."
        assert "location" in received_data, "Received data missing 'location' field."
