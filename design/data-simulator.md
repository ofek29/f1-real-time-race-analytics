# Data Simulator Design

## Overview
The data simulator is a core component for generating realistic, dynamic race telemetry data for a simulated racing environment. It focuses on providing the car's row data, which can be consumed by backend services to process and display. The following outlines the updated structure of the data simulator, including its purpose, main entities, and their attributes and methods.

---

## Purpose
The purpose of the data simulator is to:
- Generate real-time race data, such as Car speed and location.
- Enable testing and development of backend services that process this telemetry.
- Provide a foundational layer that can be extended with additional features (e.g., fuel, pit stops) as needed.

---

## Data Simulator Structure

### **Car**
Represents an individual racing car and its attributes during the simulation.

**Attributes:**
- **id**: Unique identifier for the car.
- **speed**: Current speed of the car.
- **location**: Current checkpoint on the track.

**Methods:**
- **rand_speed()**: Randomizes the car’s speed within defined limits.
- **update_location()**: Updates the car’s current checkpoint based on simulation logic.

---

## Key Features
1. **Real-Time Telemetry**: Continuously provides car speed and location updates.
2. **Foundational Design**: Can be extended to include more attributes like tire wear, fuel level, or lap times.
3. **Modular Structure**: Encapsulates car telemetry into discrete classes for maintainability.
4. **Scalability**: Supports multiple cars and checkpoints, accommodating different track configurations.