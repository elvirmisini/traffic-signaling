def reinit(streets, intersections):
    # Reinitialize mutable data structures
    for street in streets:
        street.driving_cars.clear()
        street.waiting_cars.clear()
        street.arrival_times.clear()
        street.departure_times.clear()

    for intersection in intersections:
        intersection.green_street = None
        intersection.num_waiting_cars = 0
        intersection.green_street_per_t_mod.clear()
        intersection.schedule_duration = None
        intersection.needs_updates = False


def fitness_score(schedules, streets, intersections, paths, total_duration, bonus_points,duration_to_pass_through_an_intersection):
    # we reset intersections and streets before performing a simulation
    reinit(streets, intersections)

    # save path copies to reset them after performing the simulation
    paths_copy = [path.copy() for path in paths]

    # Iterate through the schedules and initialize the intersections.
    intersection_ids_with_schedules = set()
    for schedule in schedules:
        intersection = intersections[schedule.i_intersection]
        intersection_ids_with_schedules.add(intersection.id)
        first_street = streets[schedule.order[0]]
        intersection.green_street = first_street
        intersection.needs_updates = len(schedule.order) > 1
        schedule_duration = 0
        green_street_per_t_mod = intersection.green_street_per_t_mod
        for street_id in schedule.order:
            green_time = schedule.green_times[street_id]
            for _ in range(green_time):
                green_street_per_t_mod.append(streets[street_id])
            schedule_duration += green_time
        intersection.schedule_duration = schedule_duration

    # intersection_ids_with_waiting_cars is restricted to intersections
    # with schedules
    intersection_ids_with_waiting_cars = set()
    for i_car, path in enumerate(paths):
        street = path.popleft()
        street.waiting_cars.append(i_car)
        if street.end.id in intersection_ids_with_schedules:
            intersection_ids_with_waiting_cars.add(street.end.id)
        street.end.num_waiting_cars += 1

    street_ids_with_driving_cars = set()
    score = 0

    # Main simulation loop
    for t in range(total_duration):

        # Drive across intersections
        # Store the ids of intersections that don't have waiting cars after this.
        intersection_ids_to_remove = set()
        for i_intersection in intersection_ids_with_waiting_cars:
            intersection = intersections[i_intersection]

            if intersection.needs_updates:
                # Update the green street
                t_mod = t % intersection.schedule_duration
                intersection.green_street = intersection.green_street_per_t_mod[t_mod]

            green_street = intersection.green_street
            waiting_cars = green_street.waiting_cars
            if len(waiting_cars) > 0:
                # Drive across the intersection
                waiting_car = waiting_cars.popleft()
                green_street.departure_times[waiting_car] = t
                next_street = paths[waiting_car].popleft()
                next_street.driving_cars[waiting_car] = next_street.duration
                street_ids_with_driving_cars.add(next_street.id)

                intersection.num_waiting_cars -= 1
                if intersection.num_waiting_cars == 0:
                    intersection_ids_to_remove.add(i_intersection)

        intersection_ids_with_waiting_cars.difference_update(intersection_ids_to_remove)

        # Drive across roads
        # Store the ids of streets that don't have driving cars after this.
        street_ids_to_remove = set()
        for i_street in street_ids_with_driving_cars:
            street = streets[i_street]
            driving_cars = street.driving_cars
            for car in list(driving_cars):
                # Update the "time to live" of this car, i.e. the remaining
                # driving seconds.
                ttl = driving_cars[car]
                ttl -= 1
                if ttl < 0:
                    raise ValueError
                elif ttl == 0:
                    # Reached the end of the street
                    del driving_cars[car]
                    if len(paths[car]) == 0:
                        # car finished its path
                        score += bonus_points
                        score += total_duration - t - duration_to_pass_through_an_intersection
                    else:
                        street.waiting_cars.append(car)
                        street.end.num_waiting_cars += 1
                        street.arrival_times[car] = t + 1
                        intersection_id = street.end.id
                        if intersection_id in intersection_ids_with_schedules:
                            intersection_ids_with_waiting_cars.add(intersection_id)
                else:
                    # The car is still driving on the street
                    driving_cars[car] = ttl
            if len(driving_cars) == 0:
                street_ids_to_remove.add(i_street)
        street_ids_with_driving_cars.difference_update(street_ids_to_remove)

    # The end of simulation, we reset the paths
    for i_path in range(len(paths)):
        paths[i_path] = paths_copy[i_path]
    return score
