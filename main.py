import argparse
import time

from fitness_function import fitness_score
from initial_solution import usage_based_initial_solution
from input_parser import read_input
from iterated_local_search import optimize_solution_with_ils
from ouput_writer import save_schedule_to_file


def main(instance_name, output, version_prefix) -> None:
    start_time = time.perf_counter()

    total_duration, bonus_points, intersections, streets, name_to_i_street, paths = read_input(instance_name)
    usage_based_heuristic_initial_solution = usage_based_initial_solution(intersections)

    usage_based_heuristic_initial_score = fitness_score(usage_based_heuristic_initial_solution,
                                                        streets, intersections,
                                                        paths,
                                                        total_duration,
                                                        bonus_points)
    print(f'The initial solution of {instance_name} has the score {usage_based_heuristic_initial_score}.')

    traffic_based_heuristic_initial_solution = usage_based_initial_solution(intersections)

    traffic_based_heuristic_initial_score = fitness_score(traffic_based_heuristic_initial_solution,
                                                          streets,
                                                          intersections,
                                                          paths,
                                                          total_duration,
                                                          bonus_points)
    print(f'The initial solution of {instance_name} has the score {traffic_based_heuristic_initial_score}.')

    if traffic_based_heuristic_initial_score > usage_based_heuristic_initial_score:
        initial_solution = traffic_based_heuristic_initial_solution
        initial_score = traffic_based_heuristic_initial_score
    else:
        initial_solution = usage_based_heuristic_initial_solution
        initial_score = usage_based_heuristic_initial_score

    ils_solution = optimize_solution_with_ils(initial_solution,
                                              streets,
                                              intersections,
                                              paths,
                                              total_duration,
                                              bonus_points)

    score = fitness_score(ils_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The solution of {instance_name} has the score {score}.')

    print(f'Optimized for {score - initial_score} points.')
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

# python3 main.py -i 'I180_S1080_C800.txt' -o 'I180_S1080_C800.txt' -v V7-test
# python3 main.py -i 'I2000_S12000_C57.txt' -o 'I2000_S12000_C57.txt' -v V7-test
# python3 main.py -i 'I2000_S6000_C376.txt' -o 'I2000_S6000_C376.txt' -v V7-test
# python3 main.py -i 'I200_S1000_C400.txt' -o 'I200_S1000_C400.txt' -v V7-test
# python3 main.py -i 'I200_S1000_C550.txt' -o 'I200_S1000_C550.txt' -v V7-test
# python3 main.py -i 'I200_S17200_C1000.txt' -o 'I200_S17200_C1000.txt' -v V7-test
# python3 main.py -i 'I200_S4200_C400.txt' -o 'I200_S4200_C400.txt' -v V7-test
# python3 main.py -i 'I220_S1100_C558.txt' -o 'I220_S1100_C558.txt' -v V7-test
# python3 main.py -i 'I220_S660_C430.txt' -o 'I220_S660_C430.txt' -v V7-test
