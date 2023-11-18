import os.path
from collections import deque
from recordclass import recordclass

SOLUTION_REPORTER_DIR = 'solution_reporter'
DATA_DIR = 'data'

Street = recordclass('Street', [
    'id',
    'start',
    'end',
    'name',
    'duration',
    'driving_cars',
    'waiting_cars',
    'arrival_times',
    'departure_times'
])

Intersection = recordclass('Intersection', [
    'id',
    'incomings',
    'outgoings',
    'green_street',
    'num_waiting_cars',
    'schedule_duration',
    'using_streets',
    'streets_usage',
    'green_street_per_t_mod',
    'needs_updates'
])


def read_input(instance_name: str) -> tuple:
    instance_path = os.path.join(SOLUTION_REPORTER_DIR, DATA_DIR, instance_name)

    with open(instance_path) as f:
        lines = deque(f.readlines())

    # Parse the first line
    total_duration, num_intersections, num_streets, num_cars, bonus_points = map(int, lines.popleft().split())

    intersections = tuple(Intersection(id=i,
                                       incomings=deque(),
                                       outgoings=deque(),
                                       green_street=None,
                                       num_waiting_cars=None,
                                       green_street_per_t_mod=[],
                                       schedule_duration=None,
                                       using_streets=deque(),
                                       streets_usage=dict(),
                                       needs_updates=False)
                          for i in range(num_intersections))

    streets = []
    name_to_street = {}
    for i_street in range(num_streets):
        line = lines.popleft().split()
        start, end = map(int, line[:2])
        name = line[2]
        duration = int(line[3])
        street = Street(id=i_street,
                        start=intersections[start],
                        end=intersections[end],
                        name=name,
                        duration=duration,
                        driving_cars={},
                        waiting_cars=deque(),
                        arrival_times={},
                        departure_times={})
        name_to_street[name] = street
        intersections[start].outgoings.append(street)
        intersections[end].incomings.append(street)
        streets.append(street)

    paths = []
    for i_car in range(num_cars):
        line = lines.popleft().split()
        path_length = int(line[0])
        path = line[1:]
        assert len(path) == path_length
        for name in path:
            id_inter = name_to_street[name].end.id
            intersections[id_inter].using_streets.append(name)
            if name in intersections[id_inter].streets_usage:
                intersections[id_inter].streets_usage[name] += 1
            else:
                intersections[id_inter].streets_usage[name] = 1

        path = deque(name_to_street[name] for name in path)
        paths.append(path)
    for inter in intersections:
        # delete duplicates in using_streets array
        intersections[inter.id].using_streets = list(dict.fromkeys(intersections[inter.id].using_streets))

    return total_duration, bonus_points, intersections, streets, name_to_street, paths
