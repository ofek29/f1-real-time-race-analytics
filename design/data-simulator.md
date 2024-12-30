
create an explanation for the data structure

data simulator:

Car {
    attributes:
        id
        driver
        status // 'racing', 'in pit', 'finished'
        speed
        position 
        location .:Checkpoint
        lap time // list?
        sectors time
        fuel level
        tire condition
        pit stop
    
    methods:
        rand_speed()
        calc_tire_wear()
        reduce_fuel()
        update_location()
        update_lap_time()

        pit_stop_action()
}

Checkpoint {
    id
}

Sector {
    name 
    start_checkpoint // : Checkpoint
    end_checkpoint // : Checkpoint
}

Track {
    id
    length
    sectors list
    checkpoints list

    createSectorsMap() // create sector list from checkpoints 
}

Race {
    current lap
    number of laps
    leaderboard
}

// add time?
RaceSimulationEngine:
    attributes:
        cars
        track
        race
    
    methods:
        initialize_race()
        simulate_step(): void
        update_car_states()
        check_lap_completion(car: Car): void
        check_sector_completion(car: Car): void
        generate_events(): void
        update_leaderboard()



------------------------
on client:

cars speed
Leaderboard
gaps
overtakes
pit strategy

fastest lap and sectors
