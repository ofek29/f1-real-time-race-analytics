# Application Roadmap

this is a roadmap for building Real-Time Race Event Platform. It details how to implement the microservices in the app.

---

## 1. Data Simulator
- **Objective**: Generate real-time telemetry data for cars, and send it to a Kafka topic for downstream processing.
- **Implementation**:
   - Create a Python service with models like Car and Checkpoint.
   - Simulate updates for each car at fixed intervals.
   - Publish telemetry data to a Kafka topic using the Kafka-Python library.
   - Expose API endpoints via FastAPI for starting, stopping, and monitoring the simulation.

---

## 2. Data Ingestion
- **Objective**: Receive telemetry from the Data Simulator. 
- **Implementation**:
  - Provide an HTTP endpoint or a message queue for the simulator to send data.
  - Validate and enqueue/store the incoming data for subsequent services.

---

## 3. Real-Time Processing
- **Objective**: Process incoming telemetry (e.g., update race standings, compute stats) and pass the processed data to a downstream service for delivery to the frontend.
- **Implementation**:
  - Use Node.js to consume telemetry data from Kafka.
  - Process and update race data (e.g., standings, lap progress) in real-time.
  - Forward the processed data to another service (e.g., a WebSocket or API service) for frontend consumption.

---

## 4. Telemetry Storage
- **Objective**: Store raw or processed telemetry for historical analysis.
- **Implementation**:
  - Choose a database suited for time-series or real-time data (e.g., PostgreSQL, MongoDB).
  - Design schemas to quickly query historical laps, speeds, etc.

---

## 5. Socket Service
- **Objective**: Push live telemetry to clients in real time (e.g., via WebSockets).
- **Implementation**:
  - Could be built in Node.js, Go, or Python (`asyncio`) to handle WebSocket connections.
  - Subscribe to real-time data streams and forward updates to connected clients.

---

## 6. API Gateway
- **Objective**: Provide a central HTTP entry point to access your services.
- **Implementation**:
  1. **API Setup**  
     - Create a API application (GraphQL).
     - Define routes.
  2. **Integration**  
     - The API Gateway can call the Real-Time Processing service or Telemetry Storage to fetch/update data.
     - Provide a single, consistent API for frontend or other consumers.

---

## 7. Frontend
- **Objective**: Visualize race data, car speeds, and locations.
- **Implementation**:
  - Use a modern web framework (e.g., React, Vue) to display real-time data.
  - Connect to the Socket Service (WebSockets) or periodically query the FastAPI endpoints for updates.

---

## Summary Flow

1. **Data Simulator** (Python)  
   - Generates speed/location telemetry for each car.
   - Sends data to **Data Ingestion**.

2. **Data Ingestion**  
   - Receives raw telemetry and enqueues it or passes it to **Real-Time Processing**.

3. **Real-Time Processing**  
   - Updates in-memory race data, computes live stats if necessary.
   - Stores or forwards data to **Telemetry Storage**.

4. **Telemetry Storage**  
   - Saves current/historical telemetry for later analysis or replay.

5. **Socket Service**  
   - Streams live data to connected clients.

6. **API Gateway**  
   - Offers REST endpoints for external consumers.
   - Coordinates requests to relevant internal services.

7. **Frontend**  
   - Displays real-time race information and historical insights.