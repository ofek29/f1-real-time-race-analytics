from simulator import DataSimulator
from logger import logger


def main():
    logger.info("Data Simulator started")
    simulator = DataSimulator(5)
    simulator.run()
    logger.info("Data Simulator stopped")


if __name__ == "__main__":
    main()
