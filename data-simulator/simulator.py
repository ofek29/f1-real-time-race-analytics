import json
import os
import time
from logger import logger
from models import Car
from kafka_producer import send_telemetry_data

app_mode = os.getenv("APP_RUNNING_MODE", "DEBUG")


class DataSimulator:
    def __init__(self, num_cars):
        self.cars = [Car(i) for i in range(num_cars)]

    def generate_data(self):
        for car in self.cars:
            car.randomize_speed()
            car.update_location()
            telemetry = json.dumps(
                {"id": car.id, "speed": car.speed, "location": car.location}
            )
            success = send_telemetry_data(telemetry)
            if not success:
                logger.error("Failed to send data to Kafka")
                return

    def run(self):
        if app_mode == "DEBUG":
            logger.debug("Running in DEV mode (4 laps)")
            for _ in range(4):
                self.generate_data()
                time.sleep(2)
        else:
            logger.info("Running in PROD mode (continuous)")
            while True:
                self.generate_data()
