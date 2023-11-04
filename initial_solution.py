from random import choices, randint
import random
from recordclass import recordclass

Schedule = recordclass('Schedule', [
    'i_intersection',
    'order',
    'green_times'
])


def random_initial_solution(intersections) -> Schedule:
    schedules = []
    for intersection in intersections:
        order = []
        green_times = {}
        for i in range(len(intersection.incomings)):
            green_time = choices([1, 2], weights=[90, 10], k=1)
            street = intersection.incomings[i]
            if street.name in intersection.using_streets:
                order.append(street.id)
                green_times[street.id] = int(green_time[0])
        if len(order) > 0:
            schedule = Schedule(i_intersection=intersection.id,
                                order=order,
                                green_times=green_times)
            schedules.append(schedule)
    return schedules


def traffic_based_initial_solution(intersections) -> Schedule:
    schedules = []

    # Calculate the global threshold first for efficiency
    all_waiting_cars = [len(street.waiting_cars) for intersection in intersections for street in intersection.incomings]
    threshold = sum(all_waiting_cars) / len(all_waiting_cars)

    for intersection in intersections:
        order = []
        green_times = {}

        # Sort streets based on the sum of lengths of driving_cars and waiting_cars
        sorted_streets = sorted(intersection.incomings,
                                key=lambda s: len(s.driving_cars) + len(s.waiting_cars),
                                reverse=True)

        for street in sorted_streets:
            if street.name in intersection.using_streets:
                order.append(street.id)
                # Introduce randomness in green time allocation
                random_factor = random.uniform(1, 2)  # Adjust the range as needed
                green_time = 2 if len(street.waiting_cars) > threshold else 1
                green_times[street.id] = int(green_time * random_factor)

        if order:
            schedules.append(Schedule(intersection.id, order, green_times))

    return schedules


def usage_based_initial_solution(intersections) -> Schedule:
    schedules = []

    # Calculate the global threshold_usage first for efficiency
    all_usages = [intersection.streets_usage[street.name] for intersection in intersections for street in
                  intersection.incomings if street.name in intersection.streets_usage]
    threshold_usage = sum(all_usages) / len(all_usages) if all_usages else 0

    for intersection in intersections:
        order = []
        green_times = {}

        # Sort streets based on streets_usage
        sorted_streets = sorted(intersection.incomings, key=lambda s: intersection.streets_usage.get(s.name, 0),
                                reverse=True)

        for street in sorted_streets:
            if street.name in intersection.using_streets:
                order.append(street.id)
                # Introduce randomness in green time allocation
                random_factor = random.uniform(1,2)  # Adjust the range as needed
                green_time = 2 if intersection.streets_usage.get(street.name, 0) > threshold_usage else 1
                green_times[street.id] = int(green_time * random_factor)

        if order:
            schedules.append(Schedule(intersection.id, order, green_times))

    return schedules


# import numpy as np  

# import numpy as np

# def usage_based_initial_solution(intersections, percentile=75) -> Schedule:
#     schedules = []

#     for intersection in intersections:
#         order = []
#         green_times = {}

#         # Extract street usages from valid streets
#         street_usages = [intersection.streets_usage.get(street.name, 0) for street in intersection.incomings if street.name in intersection.streets_usage]

#         if not street_usages:
#             # Handle the case where street_usages is empty (e.g., set a default threshold)
#             threshold_usage = 0
#         else:
#             # Calculate the threshold_usage based on the instance's statistics
#             threshold_usage = np.percentile(street_usages, percentile)

#         sorted_streets = sorted(intersection.incomings, key=lambda s: intersection.streets_usage.get(s.name, 0), reverse=True)

#         for street in sorted_streets:
#             if street.name in intersection.using_streets:
#                 order.append(street.id)
#                 green_times[street.id] = 2 if intersection.streets_usage.get(street.name, 0) > threshold_usage else 1

#         if order:
#             schedules.append(Schedule(intersection.id, order, green_times))

#     return schedules


from random import choices


def adapted_initial_solution(intersections) -> Schedule:
    schedules = []
    for intersection in intersections:
        # 1. Only consider the incoming streets that cars traverse
        using_incomings = [street for street in intersection.incomings if street.name in intersection.using_streets]

        # 2. Set the period of each traffic light to be equal to the number of using incoming streets
        intersection.schedule_duration = len(using_incomings)

        # Initialize green times (a dict where key is the street id and value is the green time)
        order = []
        green_times = {}
        for i, street in enumerate(using_incomings):
            order.append(street.id)
            green_times[street.id] = 1  # Each traffic light will be green for exactly 1 second

        # 3. Whenever there is a car for which the traffic light isn't scheduled, use the earliest possible time for it
        # Here, we're initializing it, so it's enough to just set a schedule for all using incoming streets
        if len(order) > 0:
            schedule = Schedule(i_intersection=intersection.id,
                                order=order,
                                green_times=green_times)
            schedules.append(schedule)

    return schedules


