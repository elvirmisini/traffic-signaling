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
    initial_solution = usage_based_initial_solution(intersections)

    initial_score = fitness_score(initial_solution, streets, intersections, paths, total_duration, bonus_points)
    print(f'The initial solution of {instance_name} has the score {initial_score}.')

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


    instancat=["I9000_S36000_C1500.txt","I10000_S30000_C1200.txt","I12000_S36000_C2000.txt"]
    for instanca in instancat:
    	for run_number in range(1, 11):
        	version = f"{args.version}_{run_number}"
        	main(instanca, instanca, version)
