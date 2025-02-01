from simulator import DataSimulator
from logger import logger

CAR_COUNT = 5  # Number of cars on track


def main():
    logger.info("Data Simulator started")
    simulator = DataSimulator(CAR_COUNT)
    simulator.run()
    logger.info("Data Simulator stopped")


if __name__ == "__main__":
    main()
