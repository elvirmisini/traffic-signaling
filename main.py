import argparse
import os.path
import time
from collections import deque

from fitness_function import fitness_score
from ils import optimize_solution_with_ils
from initial_solution import Schedule
from input_parser import read_input
from ouput_writer import save_schedule_to_file


def read_solution(solution_file_path, streets):
    with open(solution_file_path) as f:
        lines = deque(f.readlines())

    num_intersections = int(lines.popleft())

    schedules = []
    for i in range(0, num_intersections):
        i_intersection = int(lines.popleft())
        num_streets = int(lines.popleft())
        order = []
        green_times = {}
        for j in range(0, num_streets):
            street_name, green_time_str = lines.popleft().split()
            green_time = int(green_time_str)

            street_id = None
            for street in streets:
                if street.name == street_name:
                    street_id = street.id
                    break

            order.append(street_id)
            green_times[street_id] = green_time

        schedules.append(Schedule(i_intersection=i_intersection,
                                  order=order,
                                  green_times=green_times))

    return schedules


def main(instance_name, variant, version) -> None:
    start_time = time.perf_counter()

    total_duration, bonus_points, intersections, streets, name_to_i_street, paths, \
        street_id_to_car_length, intersection_id_to_car_length = read_input(instance_name)

    ssga_solution_path = os.path.join('ssga_solution', instance_name)
    initial_solution = read_solution(ssga_solution_path, streets)
    initial_score = fitness_score(initial_solution, streets, intersections, paths, total_duration, bonus_points)

    print(f'Initial Score: {initial_score}')

    ils_solution, best_solution_time, iteration, sum_all_inner_iterations = optimize_solution_with_ils(initial_solution,
                                                                                                       streets,
                                                                                                       intersections,
                                                                                                       paths,
                                                                                                       total_duration,
                                                                                                       bonus_points,
                                                                                                       street_id_to_car_length,
                                                                                                       intersection_id_to_car_length)

    score = fitness_score(ils_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {score}.')

    print(f'Optimized for {score - initial_score} points.')
    save_schedule_to_file(ils_solution,
                          streets,
                          f'{instance_name}_'
                          f'variant_{variant}_'
                          f'version_{version}_'
                          f'inner_iterations_{iteration}_'
                          f'all_iterations_{sum_all_inner_iterations}_'
                          f'best_solution_time_{best_solution_time}_'
                          f'best_score_{score}.out')

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Execution time:', elapsed_time / 60, 'minutes.\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance_name', type=str, required=True)
    parser.add_argument('-va', '--variant', type=str, required=True)
    parser.add_argument('-ve', '--version', type=str, required=True)

    args = parser.parse_args()
    main(args.instance_name, args.variant, args.version)
