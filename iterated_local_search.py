from copy import deepcopy
from random import shuffle

from fitness_function import fitness_score


def tweak(current_solution):
    new_schedule = deepcopy(current_solution)

    return new_schedule


def new_home_base(current_home_base, current_solution):
    return current_solution


def perturb(schedule):
    perturbed_schedule = deepcopy(schedule)

    for i in range(len(perturbed_schedule)):
        streets_order = perturbed_schedule[i].order
        shuffle(streets_order)  # Shuffle the order of streets.

        green_times = perturbed_schedule[i].green_times
        street_ids = list(green_times.keys())
        shuffle(street_ids)  # Shuffle the street IDs.

        for j in range(len(streets_order)):
            street_id = street_ids[j]
            perturbed_schedule[i].green_times[street_id] = green_times[streets_order[j]]

    return perturbed_schedule


def optimize_solution_with_ils(initial_solution,
                               streets,
                               intersections,
                               paths,
                               total_duration,
                               bonus_points
                               ):
    current_solution = deepcopy(initial_solution)
    current_home_base = deepcopy(initial_solution)
    best_solution = deepcopy(initial_solution)

    iteration = 0
    while iteration < 10:
        print(iteration)
        inner_iteration = 0

        while inner_iteration < 30:
            tweak_solution = perturb(current_solution)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points)
            if tw_score > cs_score:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
        if cs_score > bs_score:
            best_solution = current_solution

        current_home_base = new_home_base(current_home_base, current_solution)
        current_solution = perturb(current_home_base)
        iteration = iteration + 1

    return best_solution
