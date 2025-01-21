import random

class Car:
        def __init__(self, car_id: int, location = 0 ):
                self.id = car_id
                self.speed = 0
                self.location = location

        def randomize_speed(self):
                self.speed = random.randint(100, 130)

        def update_location(self):
                self.location += 1
                
