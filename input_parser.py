import os.path
from collections import deque
from recordclass import recordclass
import json 

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
    'needs_updates',
    'pedestrian_phase_interval',
    'all_red_phase_interval',
    'constraints'
])


def read_input(instance_name: str) -> tuple:

    filename = os.path.join(SOLUTION_REPORTER_DIR, DATA_DIR, instance_name)
    f = open(filename, 'r')

    json_file = json.load(fp=f)

    total_duration = json_file['simulation']['duration']
    num_intersections = json_file['simulation']['intersections']
    num_streets = json_file['simulation']['streets']
    num_cars = json_file['simulation']['cars']
    bonus_points = json_file['simulation']['bonus']
    duration_to_pass_through_an_intersection = json_file['simulation']['duration_to_pass_through_an_intersection']
    yellow_phase = json_file['simulation']['yellow_phase']
    limit_on_minimum_cycle_length = json_file['simulation']['limit_on_minimum_cycle_length']
    limit_on_maximum_cycle_length = json_file['simulation']['limit_on_maximum_cycle_length']
    limit_on_minimum_green_phase_duration = json_file['simulation']['limit_on_minimum_green_phase_duration']
    limit_on_maximum_green_phase_duration = json_file['simulation']['limit_on_maximum_green_phase_duration']
    intersections = tuple(Intersection(id=inter['name'],
                                       incomings=deque(),
                                       outgoings=deque(),
                                       green_street=None,
                                       num_waiting_cars=None,
                                       green_street_per_t_mod=[],
                                       schedule_duration=None,
                                       using_streets=deque(),
                                       streets_usage=dict(),
                                       needs_updates=False,
                                       pedestrian_phase_interval=inter['pedestrian_phase_interval'],
                                       all_red_phase_interval=inter['all_red_phase_interval'],                                            
                                       constraints={})
                        for inter in json_file['intersections'])
                        #   for i in range(num_intersections))
                        
    # Parse the streets
    streets = []
    name_to_street = {}
    # for i_street in range(num_streets):
    for i_street in range(0, len(json_file['streets'])): 
        s = json_file['streets'][i_street]       
        start = s['start']
        end = s['end']
        name = s['name']
        duration = s['time']

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

    # Parse the paths
    paths = []
    for i_car in range(num_cars):
        path_length = json_file['cars'][i_car]['path_length']
        path = json_file['cars'][i_car]['path']

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
    
    for constraint in json_file['constraints']:
        intersection = intersections[constraint['intersection_name']]
        if (constraint['type'] == 'simultaneously_signal'):
            if ('simultaneously_signal' in intersection.constraints):
                intersection.constraints['simultaneously_signal'].append(constraint['streets'])
            else:
                intersection.constraints['simultaneously_signal'] = [constraint['streets']]
        elif (constraint['type'] == 'signal_phase_order'):
            intersection.constraints['signal_phase_order'] = constraint['streets']
            # if ('signal_phase_order' in intersection.constraints):
            #     intersection.constraints['signal_phase_order'].append(constraint['streets'])
            # else:
            #     intersection.constraints['signal_phase_order'] = [constraint['streets']]

    for inter in intersections:
        #delete duplicates in using_streets array
        intersections[inter.id].using_streets = list(dict.fromkeys(intersections[inter.id].using_streets))
    return total_duration, bonus_points, intersections, \
           streets, name_to_street, paths, duration_to_pass_through_an_intersection, \
        yellow_phase,limit_on_minimum_cycle_length, limit_on_maximum_cycle_length, \
        limit_on_minimum_green_phase_duration, limit_on_maximum_green_phase_duration
