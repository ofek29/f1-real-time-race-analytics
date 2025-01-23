import json
import time
from models import Car
from kafka_producer import send_telemetry_data

class DataSimulator:
    def __init__(self, num_cars):
        self.cars = [Car(i) for i in range(num_cars)]

    def generate_data(self):
        for car in self.cars:
            car.randomize_speed()
            car.update_location()
            telemetry = json.dumps({"id": car.id, "speed": car.speed, "location": car.location})
            print(f"Generated telemetry data for car {car.id}: {telemetry}")
            success = send_telemetry_data(telemetry)
            print(f"Sent telemetry data for car {car.id} with success: {success}")

    def run(self):
        for i in range(4):
            self.generate_data()
            time.sleep(2)
        # while True:
        #     self.generate_data()
        #     time.sleep(1)