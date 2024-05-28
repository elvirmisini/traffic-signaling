import itertools
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
                  bonus_points: int
                  ) -> list[Schedule]:
    cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
    chb_score = fitness_score(current_home_base, streets, intersections, paths, total_duration, bonus_points)
    if cs_score >= chb_score:
        return deepcopy(current_solution)
    else:
        return deepcopy(current_home_base)


def guided_change_of_green_time(current_solution: list[Schedule],
                                street_id_to_street
                                ) -> list[Schedule]:
    tweaked_solution = deepcopy(current_solution)
    num_to_change = max(1, len(tweaked_solution) * 50 // 100)

    for _ in range(num_to_change):
        schedule = random.choice(tweaked_solution)

        if not schedule.order:
            continue

        orders = schedule.order

        new_orders = []
        for order in orders:
            if len(street_id_to_street[order].driving_cars.keys()) > 0:
                new_orders.append(order)

        if len(new_orders) == 0:
            continue

        order_to_duration = {
            order: street_id_to_street[order].duration
            for order in new_orders
        }

        order_key = max(order_to_duration, key=order_to_duration.get)

        choices = [-3] * 16 + [-2] * 17 + [-1] * 17 + [1] * 17 + [2] * 17 + [3] * 16
        change = random.choice(choices)

        schedule.green_times[order_key] = max(1, schedule.green_times[order_key] + change)

    return tweaked_solution


def change_green_times(current_solution: list[Schedule]) -> list[Schedule]:
    tweaked_solution = deepcopy(current_solution)
    num_to_change = max(1, len(tweaked_solution) * 5 // 100)
    for _ in range(num_to_change):
        schedule = random.choice(tweaked_solution)
        if not schedule.order:
            continue
        order_key = random.choice(schedule.order)
        # choices = [-1] * 40 + [1] * 40 + [2] * 10 + [3] * 5 + [4] * 5
        # choices = [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 20
        # choices = [-1] * 20 + [-2] * 20 + [-3] * 20 + [-4] * 20 + [-5] * 20
        choices = [-3] * 16 + [-2] * 17 + [-1] * 17 + [1] * 17 + [2] * 17 + [3] * 16
        change = random.choice(choices)
        schedule.green_times[order_key] = max(1, schedule.green_times[order_key] + change)
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


def optimize_orders_brute_force(current_solution: list[Schedule],
                                streets: list[Street],
                                intersections: list[Intersection],
                                paths: list[str],
                                total_duration: int,
                                bonus_points: int
                                ) -> list[Schedule]:
    best_solution = deepcopy(current_solution)
    best_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)

    num_to_optimize = max(1, len(current_solution) * 5 // 100)
    schedules_to_optimize = random.sample(current_solution, num_to_optimize)

    for schedule in schedules_to_optimize:
        original_order = schedule.order
        for i in range(len(original_order) - 2):
            # Extracting 3 continuous elements, or less if not available
            elements_to_permute = original_order[i:i + 3]
            for permuted in itertools.permutations(elements_to_permute):
                schedule.order = original_order[:i] + list(permuted) + original_order[i + 3:]
                temp_score = fitness_score(current_solution, streets, intersections, paths, total_duration,
                                           bonus_points)
                if temp_score > best_score:
                    best_score = temp_score
                    best_solution = deepcopy(current_solution)

        # Resetting the order after optimization
        schedule.order = original_order

    return best_solution


def optimize_green_times_brute_force(current_solution: list[Schedule],
                                     streets: list[Street],
                                     intersections: list[Intersection],
                                     paths: list[str],
                                     total_duration: int,
                                     bonus_points: int
                                     ) -> list[Schedule]:
    best_solution = deepcopy(current_solution)
    best_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)

    num_to_optimize = max(1, len(current_solution) * 5 // 100)
    schedules_to_optimize = random.sample(current_solution, num_to_optimize)

    for schedule in schedules_to_optimize:
        for key in schedule.green_times:
            original_value = schedule.green_times[key]
            for change in [-1, 1, 2, 3]:
                schedule.green_times[key] = max(1, original_value + change)
                temp_score = fitness_score(current_solution, streets, intersections, paths, total_duration,
                                           bonus_points)
                if temp_score > best_score:
                    best_score = temp_score
                    best_solution = deepcopy(current_solution)

            # Resetting green_times after optimization
            schedule.green_times[key] = original_value

    return best_solution


def enhanced_tweak(current_solution: list[Schedule],
                   intersection_id_to_intersection,
                   street_name_to_street,
                   street_id_to_street,
                   streets: list[Street],
                   intersections: list[Intersection],
                   paths: list[str],
                   total_duration: int,
                   bonus_points: int
                   ) -> list[Schedule]:
    # return guided_change_of_green_time(current_solution,
    #                                    street_id_to_street)
    tweak_option = random.choice([0, 1, 2, 3, 4, 5])

    if tweak_option == 0:
        return change_green_times(current_solution)
    elif tweak_option == 1:
        return swap_neighbor_orders(current_solution)
    elif tweak_option == 2:
        return guided_change_of_green_time(current_solution,
                                           street_id_to_street)
    elif tweak_option == 3:
        return optimize_orders_brute_force(current_solution,
                                           streets,
                                           intersections,
                                           paths,
                                           total_duration,
                                           bonus_points)
    elif tweak_option == 4:
        return optimize_green_times_brute_force(current_solution,
                                                streets,
                                                intersections,
                                                paths,
                                                total_duration,
                                                bonus_points)
    else:
        return swap_random_orders(current_solution)


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
                               bonus_points: int
                               ) -> list[Schedule]:
    intersection_id_to_intersection = {
        intersection.id: intersection
        for intersection in intersections
    }

    street_name_to_street = {
        street.name: street
        for street in streets
    }

    street_id_to_street = {
        street.id: street
        for street in streets
    }

    current_solution = deepcopy(initial_solution)
    current_home_base = deepcopy(initial_solution)
    best_solution = deepcopy(initial_solution)

    duration = 10 * 60

    start_time = time.time()
    iteration = 0

    while time.time() - start_time < duration:
        inner_iteration = 0
        while inner_iteration < 1000 and time.time() - start_time < duration:
            tweak_solution = enhanced_tweak(current_solution,
                                            intersection_id_to_intersection,
                                            street_name_to_street,
                                            street_id_to_street, streets, intersections, paths, total_duration,
                                            bonus_points)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points)
            if tw_score > cs_score:
                current_solution = tweak_solution
                # print('tw score:', tw_score)

            inner_iteration = inner_iteration + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
        if cs_score > bs_score:
            best_solution = current_solution
            print('bs score:', cs_score)

        current_home_base = new_home_base(current_home_base, current_solution, streets, intersections, paths,
                                          total_duration, bonus_points)
        current_solution = perturb(current_home_base)
        iteration = iteration + 1

    return best_solution

# The solution of I2000_S12000_C57.txt has the score 54495.
# Optimized for 1048 points.
# Execution time: 5.0068708216655065 minutes.

# The solution of I2000_S12000_C57.txt has the score 54496.
# Optimized for 1048 points.
# Execution time: 5.008147568333273 minutes.

# The solution of I2000_S12000_C57.txt has the score 54500.
# Optimized for 1052 points.
# Execution time: 5.0067427033325655 minutes.


