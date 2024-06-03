import argparse
import os
import time

from BeeHiveOptimization import BeeHive, usage_based_initial_solution, traffic_based_initial_solution
from GlobalFunctions import readSolution
from fitness_function import fitness_score
from input_parser import read_input
from iterated_local_search import optimize_solution_with_ils
from ouput_writer import save_schedule_to_file

SOLUTION_REPORTER_DIR = 'solution_reporter'
DATA_DIR = 'data/seed'


def main(instance_name, output, version_prefix) -> None:
    start_time = time.perf_counter()

    total_duration, bonus_points, intersections, streets, name_to_i_street, paths, \
        street_id_to_car_length, intersection_id_to_car_length = read_input(instance_name)

    # solution_file_path = os.path.join(SOLUTION_REPORTER_DIR, DATA_DIR, instance_name)
    # initial_solution = readSolution(solution_file_path=solution_file_path, streets=streets)
    usage_based_heuristic_initial_solution = usage_based_initial_solution(intersections)
    usage_based_heuristic_initial_score = fitness_score(usage_based_heuristic_initial_solution,
                                                        streets, intersections,
                                                        paths,
                                                        total_duration,
                                                        bonus_points)
    print(f'The usage based heuristic initial solution of {instance_name} has the score '
          f'{usage_based_heuristic_initial_score}.')

    traffic_based_heuristic_initial_solution = traffic_based_initial_solution(intersections)
    traffic_based_heuristic_initial_score = fitness_score(traffic_based_heuristic_initial_solution,
                                                          streets,
                                                          intersections,
                                                          paths,
                                                          total_duration,
                                                          bonus_points)
    print(f'The traffic based heuristic initial solution of {instance_name} has the score '
          f'{traffic_based_heuristic_initial_score}.')

    if traffic_based_heuristic_initial_score > usage_based_heuristic_initial_score:
        initial_solution = traffic_based_heuristic_initial_solution
    else:
        initial_solution = usage_based_heuristic_initial_solution

    il_score = fitness_score(initial_solution, streets, intersections, paths, total_duration, bonus_points)
    print('Initial score:', il_score)

    ils_solution = optimize_solution_with_ils(initial_solution,
                                              streets,
                                              intersections,
                                              paths,
                                              total_duration,
                                              bonus_points,
                                              street_id_to_car_length,
                                              intersection_id_to_car_length)

    # bee_hive_solution, bee_hive_score = BeeHive(streets, intersections, paths, total_duration, bonus_points,
    #                                             terminated_time=5 * 60,
    #                                             initial_solution=ils_solution)
    # print('ABC score:', bee_hive_score)

    score = fitness_score(ils_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {score}.')

    print(f'Optimized for {score - il_score} points.')
    save_schedule_to_file(ils_solution, streets, f"{output.replace('.txt', '')}_{version_prefix}")

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Execution time:', elapsed_time / 60, 'minutes.\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance_name', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-v', '--version', type=str, required=True)

    args = parser.parse_args()
    main(args.instance_name, args.output, args.version)

    # 1,348,502
