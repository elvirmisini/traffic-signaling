import random
from copy import deepcopy
from random import shuffle, sample

from fitness_function import fitness_score
from initial_solution import Schedule
from input_parser import Intersection, Street


def change_light_orders_and_durations(current_solution: list[Schedule]) -> list[Schedule]:
    """This operator is taken from existing literature but changed.

    Resource link: https://github.com/sagishporer/hashcode-2021-qualification
    """
    tweaked_solution = deepcopy(current_solution)

    # 1. Shuffle Green Lights for random intersections
    for i in range(len(tweaked_solution)):
        if random.random() < 0.3:  # 30% chance to shuffle an intersection
            streets_order = tweaked_solution[i].order
            shuffle(streets_order)
            tweaked_solution[i].order = streets_order

    # 2. Swap Green Light Durations for a couple of streets in some intersections
    for i in range(len(tweaked_solution)):
        green_times = tweaked_solution[i].green_times
        street_ids = list(green_times.keys())

        if len(street_ids) < 2:
            continue

        if random.random() < 0.2:  # 20% chance to swap durations for an intersection
            idx1 = random.randint(0, len(street_ids) - 1)
            idx2 = random.randint(0, len(street_ids) - 1)
            while idx1 == idx2:
                idx2 = random.randint(0, len(street_ids) - 1)

            # Swap durations
            temp_duration = green_times[street_ids[idx1]]
            green_times[street_ids[idx1]] = green_times[street_ids[idx2]]
            green_times[street_ids[idx2]] = temp_duration

    return tweaked_solution


def randomize_intersections_streets_and_customize_timings(current_solution: list[Schedule]) -> list[Schedule]:
    """Based on a comment from the link: https://codeforces.com/blog/entry/88188

    This operator changes the streets order and changes the green times by randomly
    increasing or decreasing the green time by 1 or -1.
    """
    tweaked_solution = deepcopy(current_solution)

    for i in range(len(tweaked_solution)):
        # 1. Shuffle the order of streets
        streets_order = tweaked_solution[i].order
        shuffle(streets_order)

        # 2. Modify the green times
        green_times = tweaked_solution[i].green_times

        street_ids = list(green_times.keys())
        original_total_time = sum(green_times.values())

        adjustments = []
        for _ in street_ids[:-1]:  # We don't include the last street for now
            # Change the green time a bit (either increase or decrease)
            change = random.randint(-1, 1)
            adjustments.append(change)

        # Calculate adjustment for the last street to keep total time consistent
        for street_id, adj in zip(street_ids, adjustments):
            adjustments.append(original_total_time - sum(green_times[street_id] + adj))

        for street_id, adj in zip(street_ids, adjustments):
            green_times[street_id] += adj

        # Ensure no green time goes below zero
        for street_id in street_ids:
            if green_times[street_id] < 0:
                green_times[street_id] = 0  # or reset to original

    return tweaked_solution


def randomize_intersections_streets_and_timings(current_solution: list[Schedule]) -> list[Schedule]:
    """Selects one group of intersections randomly and shuffles the order of the streets
    and changes the green light duration time.

    Example: We get a number of intersections randomly: Intersection_2, Intersection_5 and
    get the streets of these intersections for example streets of Intersection_2 are A, B, C, D.
    For these streets we have these green times: A -> 1 second, B -> 2, C -> 1, D -> 3.
    This operator will shuffle the order of the streets and changes the green duration time,
    for example the new Intersection_2 will be  B -> 1 second, D -> 3, A -> 1,C -> 1.
    """
    tweaked_solution = deepcopy(current_solution)
    for intersection in sample(tweaked_solution, k=len(tweaked_solution) // 2):
        shuffle(intersection.order)

        # Shuffle the green times for streets within an intersection
        street_ids = list(intersection.green_times.keys())
        shuffle(street_ids)
        new_green_times = {
            street_id: intersection.green_times[street_id]
            for street_id in street_ids
        }

        for street_id, green_time in intersection.green_times.items():
            intersection.green_times[street_id] = new_green_times[street_id]

    return tweaked_solution


def randomize_intersection_streets_order(current_solution: list[Schedule]) -> list[Schedule]:
    """Selects one intersection randomly and shuffles the order of how the green
    lights are going to be set for the streets.

    Example: We have an intersection Intersection_1 and its streets A, B, C, D.
    Let the current solution have the order: A, D, C, B.
    This operator will shuffle the order of the streets randomly,
    for example we will get: B, D, A, C.
    """
    tweaked_solution = deepcopy(current_solution)
    random_intersection = random.choice(tweaked_solution)
    if random_intersection.order:
        shuffle(random_intersection.order)
    return tweaked_solution


def perturb(current_solution: list[Schedule],
            streets: list[Street],
            intersections: list[Intersection],
            paths: list[str],
            total_duration: int,
            bonus_points: int
            ) -> list[Schedule]:
    """This function 'perturbs' the current traffic light scheduling solution. It randomly adjusts the green light duration
    for a street at a selected intersection and evaluates the change using a fitness score. If the new solution is not
    an improvement, the change is reverted. This process aims to iteratively enhance the traffic light schedule.
    """
    perturbed_solution = {intersection.i_intersection: intersection for intersection in current_solution}

    while True:  # This loop will run until there's no improvement
        # 1. Randomly select an intersection and a street in that intersection
        rand_intersection_id, rand_intersection = random.choice(list(perturbed_solution.items()))
        if not rand_intersection.order:
            continue
        rand_street_id = random.choice(rand_intersection.order)

        # 2. Adjust the green light time of the chosen street by ±1
        adjustment = random.choice([-1, 1])
        rand_intersection.green_times[rand_street_id] += adjustment
        rand_intersection.green_times[rand_street_id] = max(0, rand_intersection.green_times[
            rand_street_id])  # ensure non-negative

        # 3. Check if the score improves
        old_score = fitness_score(list(perturbed_solution.values()), streets, intersections, paths, total_duration,
                                  bonus_points)
        new_score = fitness_score(list(perturbed_solution.values()), streets, intersections, paths, total_duration,
                                  bonus_points)

        if new_score <= old_score:
            # If there's no improvement, revert the change and break the loop
            rand_intersection.green_times[rand_street_id] -= adjustment
            break

    return list(perturbed_solution.values())


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


def enhanced_tweak(current_solution: list[Schedule]) -> list[Schedule]:
    tweak_option = random.choice([0, 1, 2, 3])

    if tweak_option == 0:
        return randomize_intersection_streets_order(current_solution)
    elif tweak_option == 1:
        return randomize_intersections_streets_and_timings(current_solution)
    elif tweak_option == 2:
        return randomize_intersections_streets_and_customize_timings(current_solution)
    else:
        return change_light_orders_and_durations(current_solution)


def optimize_solution_with_ils(initial_solution: list[Schedule],
                               streets: list[Street],
                               intersections: list[Intersection],
                               paths: list[str],
                               total_duration: int,
                               bonus_points: int
                               ) -> list[Schedule]:
    current_solution = deepcopy(initial_solution)
    current_home_base = deepcopy(initial_solution)
    best_solution = deepcopy(initial_solution)

    iteration = 0
    while iteration < 1000:
        print('Current iteration: ', iteration)

        inner_iteration = 0
        while inner_iteration < 100:
            tweak_solution = enhanced_tweak(current_solution)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points)
            if tw_score > cs_score:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
        if cs_score > bs_score:
            best_solution = current_solution

        current_home_base = new_home_base(current_home_base, current_solution, streets, intersections, paths,
                                          total_duration, bonus_points)
        current_solution = perturb(current_home_base, streets, intersections, paths, total_duration, bonus_points)
        iteration = iteration + 1

        print('Current best score: ', bs_score)

    return best_solution
