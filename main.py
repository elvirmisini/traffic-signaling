"""
Example usage:
    python3 main.py --instance_name f.txt --output f.txt

Aliases:
    -i, --instance_name
"""
import argparse
import time

from fitness_function import fitness_score
from initial_solution import usage_based_initial_solution
from input_parser import read_input
from iterated_local_search import optimize_solution_with_ils
from ouput_writer import save_schedule_to_file


def main() -> None:
    instances = [
        "D_1700080059595.txt",
        "D_1700080080857.txt",
        "D_1700080091978.txt",
        "D_1700080114668.txt",
        "D_1700080136381.txt",
        "D_1700080157855.txt",
        "D_1700080174540.txt",
        "D_1700080186088.txt",
        "D_1700080231777.txt",
        "D_1700080788629.txt",
        "D_1700080818438.txt",
        "D_1700080856556.txt",
        "D_1700080896582.txt",
        "D_1700080929697.txt",
        "D_1700080972150.txt",
        "D_1700081036534.txt",
        "D_1700081137591.txt",
        "D_1700315814518.txt",
        "D_1700315930996.txt",
        "D_1700315996347.txt"
        # ,
        # "D_1700316031718.txt",
        # "D_1700316093211.txt",
        # "D_1700316142843.txt",
        # "D_1700316183995.txt",
        # "D_1700316231571.txt",
        # "D_1700316432224.txt",
        # "D_1700316864247.txt",
        # "D_1700316914626.txt",
        # "D_1700316947533.txt",
        # "D_1700317041227.txt",
        # "T_1700589255706.txt",
        # "T_1700589347263.txt",
        # "T_1700589526782.txt",
        # "T_1700590939595.txt",
        # "T_1700604686133.txt",
        # "T_1700604759689.txt",
        # "T_1700604810445.txt",
        # "T_1700605268629.txt",
        # "T_1700605484176.txt",
        # "T_1700606448796.txt",
        # "b.txt",
        # "c.txt",
        # "d.txt",
        # "e.txt",
        # "f.txt"
    ]

    for instance in instances:
        instance_name = instance
        output = instance

        start_time = time.perf_counter()

        total_duration, bonus_points, intersections, streets, name_to_i_street, paths = read_input(instance_name)
        initial_solution = usage_based_initial_solution(intersections)

        initial_score = fitness_score(initial_solution, streets, intersections, paths, total_duration, bonus_points)
        # print(f'The solution of {instance_name} has the score {initial_score}.')

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
        print("****************************************************************************")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--instance_name', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)

    args = parser.parse_args()
    # main(args.instance_name, args.output)
    main()
