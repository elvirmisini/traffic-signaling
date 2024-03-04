import random
import time
from copy import deepcopy

from fitness_function import fitness_score
from initial_solution import Schedule
from input_parser import Intersection, Street


def new_home_base(current_home_base: list[Schedule],
                  current_solution: list[Schedule],
                  streets: list[Street],
                  intersections: list[Intersection],
                  paths: list[str],
                  total_duration: int,
                  bonus_points: int,
                  duration_to_pass_through_an_intersection:int
                  ) -> list[Schedule]:
    cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
    chb_score = fitness_score(current_home_base, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
    if cs_score >= chb_score:
        return deepcopy(current_solution)
    else:
        return deepcopy(current_home_base)


def change_green_times(current_solution: list[Schedule],limit_on_minimum_green_phase_duration:int,limit_on_maximum_green_phase_duration:int,limit_on_minimum_cycle_length:int,limit_on_maximum_cycle_length:int) -> list[Schedule]:
    tweaked_solution = deepcopy(current_solution)
    num_to_change = max(1, len(tweaked_solution) * 5 // 100)
    for _ in range(num_to_change):
        schedule = random.choice(tweaked_solution)
        if not schedule.order:
            continue
        order_key = random.choice(schedule.order)
        choices = [-1] * 40 + [1] * 40 + [2] * 10 + [3] * 5 + [4] * 5
        change = random.choice(choices)
        current_green_time = schedule.green_times[order_key]
        new_green_time = max(min(limit_on_maximum_green_phase_duration, current_green_time + change), limit_on_minimum_green_phase_duration)
        #print(new_green_time)
        total_green_time_excluding_current = sum(green_time for street_id, green_time in schedule.green_times.items() if street_id != order_key)

        # Check if all streets except the current one have zero green time
        if total_green_time_excluding_current == 0:
            # Adjust the current street's green time to meet the cycle length constraints
            if new_green_time > limit_on_maximum_cycle_length:
                multiplier = (limit_on_maximum_cycle_length - new_green_time) / current_green_time
            elif new_green_time < limit_on_minimum_cycle_length:
                multiplier = (limit_on_minimum_cycle_length - new_green_time) / current_green_time
            else:
                multiplier = 0
        else:
            # Apply constraints on the total green time to ensure it fits within the cycle length bounds
            min_possible_total_green_time = max(limit_on_minimum_cycle_length - new_green_time, total_green_time_excluding_current)
            max_possible_total_green_time = min(limit_on_maximum_cycle_length - new_green_time, total_green_time_excluding_current)

            # Ensure new total green time stays within bounds
            total_green_time_excluding_current = max(min_possible_total_green_time, min(max_possible_total_green_time, total_green_time_excluding_current))

            # Calculate a multiplier to adjust other green times while keeping the total green time correct
            if total_green_time_excluding_current != 0:
                multiplier = total_green_time_excluding_current / sum(green_time for street_id, green_time in schedule.green_times.items() if street_id != order_key)
            else:
                multiplier = 0

        # Adjust green times for all streets except the one being changed
        for street_id in schedule.green_times:
            if street_id != order_key:
                schedule.green_times[street_id] = int(schedule.green_times[street_id] * multiplier)

        # Finally, update the green time for the street being changed
        schedule.green_times[order_key] = new_green_time
        print(schedule)
    return tweaked_solution



def swap_neighbor_orders(current_solution: list[Schedule]) -> list[Schedule]:
    tweaked_solution = deepcopy(current_solution)
    num_to_swap = max(1, len(tweaked_solution) * 5 // 100)
    for _ in range(num_to_swap):
        schedule = random.choice(tweaked_solution)
        if len(schedule.order) > 1:
            index = random.randint(0, len(schedule.order) - 2)
            schedule.order[index], schedule.order[index + 1] = schedule.order[index + 1], schedule.order[index]
    return tweaked_solution


def swap_random_orders(current_solution: list[Schedule]) -> list[Schedule]:
    tweaked_solution = deepcopy(current_solution)
    num_to_swap = max(1, len(tweaked_solution) * 5 // 100)
    for _ in range(num_to_swap):
        schedule = random.choice(tweaked_solution)
        if len(schedule.order) > 1:
            index1, index2 = random.sample(range(len(schedule.order)), 2)
            schedule.order[index1], schedule.order[index2] = schedule.order[index2], schedule.order[index1]
    return tweaked_solution


def enhanced_tweak(current_solution: list[Schedule],limit_on_minimum_green_phase_duration:int,limit_on_maximum_green_phase_duration:int,limit_on_minimum_cycle_length:int,limit_on_maximum_cycle_length:int) -> list[Schedule]:
    tweak_option = random.random()

    if tweak_option < 0.45:
        return swap_neighbor_orders(current_solution)
    elif tweak_option < 0.90:
        return swap_random_orders(current_solution)
    else:
        return change_green_times(current_solution,limit_on_minimum_green_phase_duration,limit_on_maximum_green_phase_duration)


def perturb(current_solution: list[Schedule]) -> list[Schedule]:
    perturbed_solution = deepcopy(current_solution)
    num_to_shuffle = max(1, len(perturbed_solution) * 20 // 100)
    for _ in range(num_to_shuffle):
        schedule = random.choice(perturbed_solution)
        random.shuffle(schedule.order)
    return perturbed_solution


def optimize_solution_with_ils(initial_solution: list[Schedule],
                               streets: list[Street],
                               intersections: list[Intersection],
                               paths: list[str],
                               total_duration: int,
                               bonus_points: int,
                               limit_on_minimum_green_phase_duration:int,
                               limit_on_maximum_green_phase_duration:int,
                               duration_to_pass_through_an_intersection:int,
                               limit_on_minimum_cycle_length:int,
                               limit_on_maximum_cycle_length:int
                               ) -> list[Schedule]:
    current_solution = deepcopy(initial_solution)
    current_home_base = deepcopy(initial_solution)
    best_solution = deepcopy(initial_solution)

    duration = 1 * 60

    start_time = time.time()
    iteration = 0

    while time.time() - start_time < duration:
        inner_iteration = 0
        while inner_iteration < 100 and time.time() - start_time < duration:
            tweak_solution = enhanced_tweak(current_solution,limit_on_minimum_green_phase_duration,limit_on_maximum_green_phase_duration,limit_on_minimum_cycle_length,limit_on_maximum_cycle_length)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
            if tw_score > cs_score:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection)
        if cs_score > bs_score:
            best_solution = current_solution

        current_home_base = new_home_base(current_home_base, current_solution, streets, intersections, paths,
                                          total_duration, bonus_points,duration_to_pass_through_an_intersection)
        current_solution = perturb(current_home_base)
        iteration = iteration + 1

    return best_solution
