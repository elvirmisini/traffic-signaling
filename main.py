"""

Example usage:
    python3 main.py --instance_name a.txt --output a.txt

Aliases:
    -i, --instance_name
"""

import argparse
import time

from fitness_function import fitness_score
from initial_solution import random_initial_solution, traffic_based_initial_solution, \
    usage_based_initial_solution, adapted_initial_solution
from input_parser import read_input
from iterated_local_search import optimize_solution_with_ils
from ouput_writer import save_schedule_to_file


def main(instance_name: str, output: str) -> None:
    start_time = time.perf_counter()

    total_duration, bonus_points, intersections, streets, name_to_i_street, paths = read_input(instance_name)
    initial_solution = usage_based_initial_solution(intersections)

    initial_score = fitness_score(initial_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {initial_score}.')

    ils_solution = optimize_solution_with_ils(initial_solution,
                                              streets,
                                              intersections,
                                              paths,
                                              total_duration,
                                              bonus_points)

    score = fitness_score(ils_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {score}.')

    print(f'\nOptimized for {score - initial_score} points.')
    save_schedule_to_file(ils_solution, streets, output)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Execution time:', elapsed_time / 60, 'minutes.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance_name', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)

    args = parser.parse_args()
    main(args.instance_name, args.output)
