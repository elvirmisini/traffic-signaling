from copy import deepcopy

from fitness_function import fitness_score


def tweak(current_solution):
    new_schedule = deepcopy(current_solution)

    return new_schedule


def new_home_base(current_home_base, current_solution):
    return current_solution


def perturb(current_home_base):
    return current_home_base


def optimize_solution_with_ils(initial_solution,
                               streets,
                               intersections,
                               paths,
                               total_duration,
                               bonus_points
                               ):
    current_solution = initial_solution
    current_home_base = initial_solution
    best_solution = initial_solution

    iteration = 0
    while iteration < 1000:
        inner_iteration = 0

        while inner_iteration < 1000:
            tweak_solution = tweak(current_solution)

            if fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points) - \
                    fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points) > 0:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1

        if fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points) - \
                fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points) > 0:
            best_solution = current_solution

        current_home_base = new_home_base(current_home_base, current_solution)
        current_solution = perturb(current_home_base)

    return best_solution
