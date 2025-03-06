import os
import json
import pytest
import subprocess
from confluent_kafka import Consumer
from logger import logger

# Test configuration
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
topic_name = "telemetry_row_data"
CAR_COUNT = 5  # Same as in main.py
NUMBER_OF_LAPS = 4  # Same as in simulator.py


def test_simulator_e2e():
    """
    End-to-end test for the simulator:
    1. Run main file with APP_RUNNING_MODE=DEBUG
    2. Wait for it to finish (4 laps)
    3. Setup consumer and read all messages
    4. Verify message fields and location updates
    """
    # Set environment variables
    env = os.environ.copy()
    env["APP_RUNNING_MODE"] = "DEBUG"
    env["KAFKA_BOOTSTRAP_SERVERS"] = bootstrap_servers

    # Path to main.py relative to the test file
    main_script_path = os.path.join(os.path.dirname(__file__), "..", "main.py")

    # Run the main script and wait for it to complete
    logger.info("Starting simulator application")
    process = subprocess.Popen(
        ["python", main_script_path],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for process to complete
    stdout, stderr = process.communicate()
    combined_output = stdout + stderr

    # Check process exit code
    assert (
        process.returncode == 0
    ), f"Process failed with exit code {process.returncode}"

    # Verify log messages
    assert "Data Simulator started" in combined_output, "Missing startup log message"
    assert "Running in DEV mode" in combined_output, "Missing debug mode log"
    assert "Data Simulator stopped" in combined_output, "Missing shutdown log message"

    logger.info("Simulator completed successfully, now setting up consumer")

    # Now setup the consumer to read the produced messages
    consumer_config = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": "test-consumer",
        "auto.offset.reset": "earliest",  # Start from beginning of topic
    }

    consumer = Consumer(consumer_config)
    consumer.subscribe([topic_name])

    # Telemetry data storage
    car_messages = {}

    # Keep collecting messages until we have all expected data or run out of messages
    expected_message_count = CAR_COUNT * NUMBER_OF_LAPS
    message_count = 0

    logger.info(f"Expecting {expected_message_count} messages (cars × laps)")

    # Poll for messages
    while message_count < expected_message_count:
        msg = consumer.poll(1.0)

        if msg is None:
            pytest.fail("Timeout: No message received when expected.")

        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            raise Exception(msg.error())

        # Process the message
        message_count += 1
        value = msg.value().decode("utf-8")
        data = json.loads(value)

        # Track this message by car ID for later validation
        car_id = data["id"]
        if car_id not in car_messages:
            car_messages[car_id] = []
        car_messages[car_id].append(data)

        logger.info(
            f"Received message {message_count}: Car {car_id}, Location {data['location']}"
        )

    # Close consumer after polling
    consumer.close()

    # Verify we received messages for all cars
    assert (
        len(car_messages) == CAR_COUNT
    ), f"Expected data from {CAR_COUNT} cars, got {len(car_messages)}"

    # Check each car's data
    for car_id, messages in car_messages.items():
        # Sort messages by location to ensure we check in sequence
        messages.sort(key=lambda x: x["location"])

        # Verify we have the expected number of messages per car
        assert (
            len(messages) == NUMBER_OF_LAPS
        ), f"Car {car_id} has {len(messages)} messages, expected {NUMBER_OF_LAPS}"

        # Check location increment
        for i, data in enumerate(messages):
            # Verify message structure
            assert "id" in data, f"Message missing 'id' field: {data}"
            assert "speed" in data, f"Message missing 'speed' field: {data}"
            assert "location" in data, f"Message missing 'location' field: {data}"

            # Check location is updated by 1 each lap
            expected_location = i + 1  # Location starts at 1 and increments by 1
            assert (
                data["location"] == expected_location
            ), f"Car {car_id} at lap {i+1} has location {data['location']}, expected {expected_location}"

    logger.info(
        f"Successfully validated data for {len(car_messages)} cars across {NUMBER_OF_LAPS} laps"
    )
