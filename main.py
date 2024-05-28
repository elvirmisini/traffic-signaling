import time

from fitness_function import fitness_score
from initial_solution import traffic_based_initial_solution, usage_based_initial_solution
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
        initial_score = traffic_based_heuristic_initial_score
    else:
        initial_solution = usage_based_heuristic_initial_solution
        initial_score = usage_based_heuristic_initial_score

    # try to remove all the streets and intersections without cars

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
    instance_names = [
        # "I70_S210_C200.txt",
        # "I99_S399_C400.txt",
        # "I100_S600_C153.txt",
        # "I120_S480_C500.txt",
        # "I180_S1080_C800.txt",
        # "I200_S4200_C400.txt",
        # "I241_S43241_C158.txt",
        # "I300_S900_C500.txt",
        # "I400_S2400_C944.txt",
        # "I444_S1776_C666.txt",
        # "I500_S2000_C315.txt",
        # "I600_S3000_C332.txt",
        # "I1662_S10000_C1000.txt",
        # "I2500_S10000_C306.txt",
        # "I3000_S18000_C227.txt",
        # "I4000_S12000_C161.txt",
        # "I7073_S9102_C1000.txt",
        # "I8000_S95928_C1000.txt",
        # "I10000_S35030_C1000.txt",
        # "I12000_S36000_C2000.txt"
        # 'a_an_example.txt'
        "I2000_S12000_C57.txt"
    ]

    versions = [
        "V1"
        # ,
        # "V2",
        # "V3",
        # "V4",
        # "V5"
    ]

    for instance_name in instance_names:
        for version in versions:
            main(instance_name, instance_name, version)
