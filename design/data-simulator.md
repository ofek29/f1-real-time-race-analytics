# Data Simulator Design

## Overview
The data simulator is a core component for generating realistic, dynamic race telemetry data for a simulated racing environment. It models cars, track details, and race behavior to provide a rich dataset for backend services to process and display. The following outlines the structure of the data simulator, including its purpose, main entities, and their attributes and methods.

---

## Purpose
The purpose of the data simulator is to:
- Generate real-time race data, including car speeds, positions, and lap times.
- Simulate physical effects like fuel consumption and tire wear.
- Enable testing and development of backend services that process race telemetry.
- Provide realistic behavior for pit stops and other race events.

---

## Data Simulator Structure

### **Car**
Represents an individual racing car and its attributes during the simulation.

**Attributes:**
- `id`: Unique identifier for the car.
- `driver`: Driver name or ID.
- `status`: Current status of the car (`'racing'`, `'in pit'`, `'finished'`).
- `speed`: Current speed of the car.
- `position`: Current track position.
- `location`: Current checkpoint on the track.
- `lap_time`: Records lap times (can be stored as a list for historical data).
- `sectors_time`: Records sector times for the current lap.
- `fuel_level`: Current fuel level as a percentage.
- `tire_condition`: Current tire wear as a percentage.
- `pit_stop`: Tracks the number of pit stops made.

**Methods:**
- `rand_speed()`: Randomizes the car’s speed within limits based on conditions.
- `calc_tire_wear()`: Calculates tire degradation over time.
- `reduce_fuel()`: Simulates fuel consumption based on speed and time.
- `update_location()`: Updates the car’s current position and checkpoint.
- `update_lap_time()`: Updates lap and sector times.
- `pit_stop_action()`: Handles refueling, tire changes, and pit stop timing.

---

### **Checkpoint**
Defines a specific location on the track.

**Attributes:**
- `id`: Unique identifier for the checkpoint.

---

### **Sector**
Represents a section of the track between two checkpoints.

**Attributes:**
- `name`: Name of the sector (e.g., Sector 1, Sector 2).
- `start_checkpoint`: Starting checkpoint for the sector.
- `end_checkpoint`: Ending checkpoint for the sector.

---

### **Track**
Defines the entire race track, including sectors and checkpoints.

**Attributes:**
- `id`: Unique identifier for the track.
- `length`: Total track length in meters.
- `sectors_list`: List of `Sector` objects.
- `checkpoints_list`: List of `Checkpoint` objects.

**Methods:**
- `create_sectors_map()`: Generates the sector list from the provided checkpoints.

---

### **Race**
Tracks the state of the race.

**Attributes:**
- `current_lap`: Current lap number in the race.
- `number_of_laps`: Total laps in the race.
- `leaderboard`: Current standings of the cars.

---

### **RaceSimulationEngine**
Orchestrates the entire simulation process.

**Attributes:**
- `cars`: List of `Car` objects participating in the race.
- `track`: The `Track` object for the race.
- `race`: The `Race` object to manage race state.

**Methods:**
- `initialize_race()`: Initializes cars, track, and race parameters.
- `start_race()`: Starts the simulation loop.
- `update_car_states()`: Updates the states of all cars (speed, fuel, tire wear, etc.).
- `check_lap_completion()`: Checks if a car has completed a lap and updates its status.
- `check_sector_completion()`: Checks if a car has completed a sector and updates times.
- `update_leaderboard()`: Updates the race leaderboard based on car progress.

---

## Key Features
1. **Real-Time Simulation:** Models dynamic race conditions, such as varying speeds and sector times.
2. **Event Handling:** Simulates events like pit stops and fuel depletion.
3. **Modular Design:** Encapsulates logic into discrete classes for maintainability.
4. **Scalability:** Supports multiple cars and tracks with varied configurations.