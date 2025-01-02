
# Data Simulator Service Roadmap

## Overview
The **Data Simulator Service** is responsible for generating real-time telemetry data for cars in a racing environment. It simulates attributes like speed and location and sends this data to a Kafka topic for downstream services to process.

---

## Objectives
- Simulate car telemetry in real time, including:
  - **Attributes:** `id`, `speed`, `location`.
  - **Methods:** Random speed generation and location updates.
- Send telemetry data to a Kafka topic.
- Provide an API for managing the simulation and monitoring its status.

---

## Features
1. **Real-Time Telemetry Generation**
   - Generates realistic car data in a racing simulation.
   - Periodically updates each car’s speed and location.

2. **Kafka Integration**
   - Publishes telemetry data to a configurable Kafka topic for further processing.

3. **Management and Monitoring API**
   - Start/stop the simulation.
   - Retrieve the current status of the simulation.

4. **Continuous Integration**
   - Automated pipelines for testing and validating code changes.

---

## Technology Stack
- **Python**: Core programming language.
- **FastAPI**: For API management and monitoring.
- **Kafka-Python**: Library for Kafka integration.

---

## Roadmap

### Phase 1: Service Initialization
1. **Define Models**
   - Create models for `Car` and `Checkpoint`:
     - `Car` includes attributes: `id`, `speed`, and `location`.
     - `Checkpoint` represents track positions.
   - Add methods for generating speed and updating locations.

2. **Set Up Kafka Integration**
   - Configure a Kafka producer to send telemetry data.
   - Define the structure of telemetry messages (e.g., JSON format).

3. **Implement Simulation Logic**
   - Develop a simulator that updates car telemetry in real time.
   - Add a loop to generate data at fixed intervals.

---

### Phase 2: API Development
1. **FastAPI Setup**
   - Create API endpoints for:
     - Starting the simulation (`POST /start`).
     - Stopping the simulation (`POST /stop`).
     - Checking the status of the simulator (`GET /status`).

2. **Background Task Integration**
   - Use FastAPI’s background tasks to run the simulator independently of API calls.

---

### Phase 3: Testing and Validation
1. **Unit Tests**
   - Test all models for correct behavior (e.g., speed generation, location updates).
   - Validate Kafka message formatting and sending.

2. **Integration Tests**
   - Test the full pipeline: data generation → Kafka → downstream consumer.

3. **API Testing**
   - Verify that API endpoints start, stop, and report the simulator’s status as expected.

---

### Phase 4: Continuous Integration
1. **Set Up GitHub Actions**
   - Create a `.github/workflows/ci.yml` file to automate testing and code validation.

2. **Integrate CI with Pull Requests**
   - Require successful CI checks before merging code into the main branch.

---

## Deliverables
1. **Real-Time Telemetry Generator**
   - A Python-based simulator that generates and sends telemetry data to Kafka.

2. **API for Simulation Management**
   - Start, stop, and monitor the simulation via HTTP endpoints.

3. **Kafka Topic Integration**
   - Publish car telemetry data in real time to a specified Kafka topic.
