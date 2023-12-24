import argparse
import csv
import os
import re


def parse_simulation_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    simulation_data = list(map(int, lines[0].split()))
    simulation_time, intersections, streets, cars, bonus_points = simulation_data[:5]

    total_travel_time = 0
    for line in lines[1:]:
        parts = line.split()
        travel_time_match = re.search(r'\d+', parts[-1])
        if travel_time_match:
            total_travel_time += int(travel_time_match.group())

    average_travel_time = float(total_travel_time) / float(cars) if cars else 0

    return {
        'Instance': os.path.basename(file_path).replace('.txt', ''),
        'Simulation Time': simulation_time,
        'Intersections': intersections,
        'Streets': streets,
        'Cars': cars,
        'Bonus Points': bonus_points,
        'Average Travel Time': average_travel_time
    }


def main(input_dir, output_path):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.txt')]
    instances_data = [parse_simulation_data(file_path) for file_path in files]

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Instance', 'Simulation Time', 'Intersections', 'Streets', 'Cars', 'Bonus Points',
                      'Average Travel Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for instance in instances_data:
            writer.writerow(instance)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Parse simulation data and output to CSV.')
    # parser.add_argument('input_dir', type=str, help='Directory containing the text files.')
    # parser.add_argument('output_path', type=str, help='Output path for the CSV file.')
    # args = parser.parse_args()

    # input_dir = '/home/uranlajci/Downloads/instancat'
    output_path = '/home/uranlajci/Documents/GitHub/traffic-signaling/output.csv'
    main(input_dir, output_path)
