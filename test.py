
import json

# Read JSON data from file
with open("solution_reporter/data/test1.json", "r") as file:
    data = file.read()

parsed_data = json.loads(data)

# Extract simulation data
simulation = parsed_data['simulation']
duration = simulation['duration']
intersections = len(parsed_data['intersections'])
streets = simulation['streets']
cars = simulation['cars']
bonus = simulation['bonus']
duration_to_pass_through_an_intersection = simulation['duration_to_pass_through_an_intersection']
yellow_phase = simulation['yellow_phase']
limit_on_minimum_cycle_length = simulation['limit_on_minimum_cycle_length']
limit_on_maximum_cycle_length = simulation['limit_on_maximum_cycle_length']
limit_on_minimum_green_phase_duration = simulation['limit_on_minimum_green_phase_duration']
limit_on_maximum_green_phase_duration = simulation['limit_on_maximum_green_phase_duration']

# Write simulation data to txt file
with open("output.txt", "w") as txt_file:
    txt_file.write(f"{duration} {intersections} {streets} {cars} {bonus} {duration_to_pass_through_an_intersection} {yellow_phase} {limit_on_minimum_cycle_length} {limit_on_maximum_cycle_length} {limit_on_minimum_green_phase_duration} {limit_on_maximum_green_phase_duration}\n")
    
    # Write street data to txt file
    for street in parsed_data['streets']:
        txt_file.write(f"{street['start']} {street['end']} {street['name']} {street['time']}\n")
    
    # Write car data to txt file
    for car in parsed_data['cars']:
        path = ' '.join(car['path'])
        txt_file.write(f"{len(car['path'])} {path}\n")
        
    for intersections in parsed_data['intersections']:
        txt_file.write(f"{intersections['name']} {intersections['pedestrian_phase_interval']} {intersections['all_red_phase_interval']}\n")
