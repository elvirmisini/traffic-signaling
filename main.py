import argparse
import time

from fitness_function import fitness_score
from ils import optimize_solution_with_ils
from initial_solution import usage_based_initial_solution
from input_parser import read_input
from ouput_writer import save_schedule_to_file


def main(instance_name, variant, version) -> None:
    start_time = time.perf_counter()

    total_duration, bonus_points, intersections, streets, name_to_i_street, paths, \
        street_id_to_car_length, intersection_id_to_car_length = read_input(instance_name)

    usage_based_heuristic_initial_solution = usage_based_initial_solution(intersections)
    usage_based_heuristic_initial_score = fitness_score(usage_based_heuristic_initial_solution,
                                                        streets, intersections,
                                                        paths,
                                                        total_duration,
                                                        bonus_points)
    print(f'The usage based heuristic initial solution of {instance_name} has the score '
          f'{usage_based_heuristic_initial_score}.')

    # traffic_based_heuristic_initial_solution = traffic_based_initial_solution(intersections)
    # traffic_based_heuristic_initial_score = fitness_score(traffic_based_heuristic_initial_solution,
    #                                                       streets,
    #                                                       intersections,
    #                                                       paths,
    #                                                       total_duration,
    #                                                       bonus_points)
    # print(f'The traffic based heuristic initial solution of {instance_name} has the score '
    #       f'{traffic_based_heuristic_initial_score}.')

    ils_solution, best_solution_time, iteration, sum_all_inner_iterations = optimize_solution_with_ils(
        usage_based_heuristic_initial_solution,
        streets,
        intersections,
        paths,
        total_duration,
        bonus_points,
        street_id_to_car_length,
        intersection_id_to_car_length)

    score = fitness_score(ils_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {score}.')

    print(f'Optimized for {score - usage_based_heuristic_initial_score} points.')
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
