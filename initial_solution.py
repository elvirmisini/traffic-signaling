import math
import random
from recordclass import recordclass
from input_parser import Intersection

Schedule = recordclass('Schedule', [
    'i_intersection',
    'order',
    'green_times'
])

def traffic_based_initial_solution(intersections: list[Intersection]) -> list[Schedule]:
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


def usage_based_initial_solution(intersections: list[Intersection]) -> list[Schedule]:
    schedules = []
    for intersection in intersections:
        order = []
        green_times = {}

        sorted_streets = sorted(intersection.incomings, key=lambda s: intersection.streets_usage.get(s.name, 0),
                                reverse=True)

        for street in sorted_streets:
            if street.name in intersection.using_streets:
                order.append(street.id)
                usage = intersection.streets_usage.get(street.name, 0)
                green_time = int(math.sqrt(usage)) if usage > 0 else 1
                green_times[street.id] = green_time

        if order:
            schedules.append(Schedule(intersection.id, order, green_times))
    return schedules