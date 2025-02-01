import json
import time
from logger import logger
from models import Car
from kafka_producer import send_telemetry_data


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
        for _ in range(4):
            self.generate_data()
            time.sleep(2)
        # while True:
        #     self.generate_data()
        #     time.sleep(1)
