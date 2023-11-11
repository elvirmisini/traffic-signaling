import random
from copy import deepcopy
from random import shuffle, sample

from fitness_function import fitness_score


def shuffle_and_adjust_timings(current_solution):
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


def tweak_light_order_and_duration(schedule):
    """This operator is taken from existing literature but changed.

    Resource link: https://github.com/sagishporer/hashcode-2021-qualification
    """
    perturbed_schedule = deepcopy(schedule)

    # 1. Shuffle Green Lights for random intersections
    for i in range(len(perturbed_schedule)):
        if random.random() < 0.3:  # 30% chance to shuffle an intersection
            streets_order = perturbed_schedule[i].order
            shuffle(streets_order)
            perturbed_schedule[i].order = streets_order

    # 2. Swap Green Light Durations for a couple of streets in some intersections
    for i in range(len(perturbed_schedule)):
        green_times = perturbed_schedule[i].green_times
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

    return perturbed_schedule


def tweak_showtime(current_solution, streets, intersections, paths, total_duration, bonus_points):
    tweaked_solution = deepcopy(current_solution)
    rand_intersection = random.choice(tweaked_solution)
    if rand_intersection.order:
        shuffle(rand_intersection.order)
    return tweaked_solution


def shuffle_single_intersection_order(schedule):
    perturbed_schedule = deepcopy(schedule)

    # Example: Shuffle the order of streets within a random subset of intersections
    for intersection in sample(perturbed_schedule, k=len(perturbed_schedule) // 2):
        shuffle(intersection.order)
        shuffle_green_times(intersection.green_times)

    return perturbed_schedule


def enhanced_tweak(current_solution, streets, intersections, paths, total_duration, bonus_points):
    tweak_option = random.choice(
        ["showtime", "single_shuffle", "adjust_timings", "light_order_duration", "switch_green_times"])

    if tweak_option == "showtime":
        return tweak_showtime(current_solution, streets, intersections, paths, total_duration, bonus_points)
    elif tweak_option == "single_shuffle":
        return shuffle_single_intersection_order(current_solution)
    elif tweak_option == "adjust_timings":
        return shuffle_and_adjust_timings(current_solution)
    elif tweak_option == "switch_green_times":  # added new
        return switch_green_times(current_solution)
    else:  # "light_order_duration"
        return tweak_light_order_and_duration(current_solution)


def new_home_base(current_home_base, current_solution, streets, intersections, paths, total_duration, bonus_points):
    cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
    chb_score = fitness_score(current_home_base, streets, intersections, paths, total_duration, bonus_points)
    if cs_score >= chb_score:
        return deepcopy(current_solution)
    else:
        return deepcopy(current_home_base)


def perturb(current_solution, streets, intersections, paths, total_duration, bonus_points):
    tweaked_solution = {intersection.i_intersection: intersection for intersection in current_solution}

    while True:  # This loop will run until there's no improvement
        # 1. Randomly select an intersection and a street in that intersection
        rand_intersection_id, rand_intersection = random.choice(list(tweaked_solution.items()))
        if not rand_intersection.order:
            continue
        rand_street_id = random.choice(rand_intersection.order)

        # 2. Adjust the green light time of the chosen street by ±1
        adjustment = random.choice([-1, 1])
        rand_intersection.green_times[rand_street_id] += adjustment
        rand_intersection.green_times[rand_street_id] = max(0, rand_intersection.green_times[
            rand_street_id])  # ensure non-negative

        # 3. Check if the score improves
        old_score = fitness_score(list(tweaked_solution.values()), streets, intersections, paths, total_duration,
                                  bonus_points)
        new_score = fitness_score(list(tweaked_solution.values()), streets, intersections, paths, total_duration,
                                  bonus_points)

        if new_score <= old_score:
            # If there's no improvement, revert the change and break the loop
            rand_intersection.green_times[rand_street_id] -= adjustment
            break

    return list(tweaked_solution.values())


def switch_green_times(schedule):
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


def shuffle_green_times(green_times):
    # Shuffle the green times for streets within an intersection
    street_ids = list(green_times.keys())
    shuffle(street_ids)
    new_green_times = {street_id: green_times[street_id] for street_id in street_ids}

    for street_id, green_time in green_times.items():
        green_times[street_id] = new_green_times[street_id]


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
    while iteration < 1000:
        print(iteration)
        inner_iteration = 0
        i = 0
        while inner_iteration < 1000:
            tweak_solution = enhanced_tweak(current_solution, streets, intersections, paths, total_duration,
                                            bonus_points)

            cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
            tw_score = fitness_score(tweak_solution, streets, intersections, paths, total_duration, bonus_points)
            if tw_score > cs_score:
                current_solution = tweak_solution

            inner_iteration = inner_iteration + 1
            if i == 0:
                print(tw_score)
            i = i + 1

        bs_score = fitness_score(best_solution, streets, intersections, paths, total_duration, bonus_points)
        cs_score = fitness_score(current_solution, streets, intersections, paths, total_duration, bonus_points)
        if cs_score > bs_score:
            best_solution = current_solution

        print('Best Score: ', bs_score)
        current_home_base = new_home_base(current_home_base, current_solution, streets, intersections, paths,
                                          total_duration, bonus_points)
        current_solution = perturb(current_home_base, streets, intersections, paths, total_duration, bonus_points)
        iteration = iteration + 1

    return best_solution
