
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

# Write simulation data to txt file
with open("output.txt", "w") as txt_file:
    txt_file.write(f"{duration} {intersections} {streets} {cars} {bonus}\n")
    
    # Write street data to txt file
    for street in parsed_data['streets']:
        txt_file.write(f"{street['start']} {street['end']} {street['name']} {street['time']}\n")
    
    # Write car data to txt file
    for car in parsed_data['cars']:
        path = ' '.join(car['path'])
        txt_file.write(f"{len(car['path'])} {path}\n")
