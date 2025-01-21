from simulator import DataSimulator

simulator = DataSimulator(5)

def main():
    print("Starting data generation")
    simulator.run()
    print("Data generation complete")

if __name__ == "__main__":
    main()