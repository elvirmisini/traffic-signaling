from copy import deepcopy
from random import shuffle

from fitness_function import fitness_score

import random


def tweak(current_solution):
    modified_schedule = deepcopy(current_solution)

    for i in range(len(modified_schedule)):
        # 1. Shuffle the order of streets
        streets_order = modified_schedule[i].order
        shuffle(streets_order)

        # 2. Modify the green times
        green_times = modified_schedule[i].green_times

        street_ids = list(green_times.keys())
        original_total_time = sum(green_times.values())

        adjustments = []
        for _ in street_ids[:-1]:  # We don't include the last street for now
            # Change the green time a bit (either increase or decrease)
            change = random.randint(-2, 2)  # You can adjust these values as needed
            adjustments.append(change)

        # Calculate adjustment for the last street to keep total time consistent
        adjustments.append(
            original_total_time - sum(green_times[street_id] + adj for street_id, adj in zip(street_ids, adjustments)))

        for street_id, adj in zip(street_ids, adjustments):
            green_times[street_id] += adj

        # Ensure no green time goes below zero
        for street_id in street_ids:
            if green_times[street_id] < 0:
                green_times[
                    street_id] = 0  # or reset to original: green_times[street_id] = schedule[i].green_times[street_id]

    return modified_schedule


# def new_home_base(current_home_base, current_solution):
#     return current_solution


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
    while iteration < 20:
        print(iteration)
        inner_iteration = 0

        while inner_iteration < 20:
            tweak_solution = tweak(current_solution)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points)
            if tw_score > cs_score:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
        if cs_score > bs_score:
            best_solution = current_solution

        # current_home_base = new_home_base(current_home_base, current_solution)
        current_solution = perturb(current_solution)
        iteration = iteration + 1

    return best_solution
