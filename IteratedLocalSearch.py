import GlobalFunctions as gl

from random import sample, choices, shuffle
from time import time
from copy import deepcopy
from recordclass import recordclass

Schedule = recordclass('Schedule', [
    'i_intersection',
    'order',
    'green_times'
])


def randomSolution(intersections):
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
# Define a perturbation function for ILS.
def perturbSchedule(schedule, streets, intersections):
    # Implement your perturbation strategy here.
    # For example, you can randomly change the timing of traffic signals.
    perturbed_schedule = deepcopy(schedule)
    # Modify the schedule in a way that introduces diversity.
    return perturbed_schedule



# Define a local search function for ILS.
def localSearch(schedule, streets, intersections, paths, total_duration, bonus_points):
    # Implement your local search method here to improve the given schedule.
    # You can use any local search algorithm suitable for your problem.
    improved_schedule = deepcopy(schedule)
    # Apply local search operations to improve the schedule.
    return improved_schedule

# Modify your main ILS function.
def ILS(streets, intersections, paths, total_duration, bonus_points, terminated_time, max_iterations):
    current_schedule = randomSolution(intersections)
    best_schedule = deepcopy(current_schedule)
    best_score = gl.grade(current_schedule, streets, intersections, paths, total_duration, bonus_points)
    
    while (time() - terminated_time < 10):
        # 1. Perturbation
        perturbed_schedule = perturbSchedule(current_schedule, streets, intersections)
        
        # 2. Local Search
        improved_schedule = localSearch(perturbed_schedule, streets, intersections, paths, total_duration, bonus_points)
        
        # 3. Acceptance Criterion
        new_score = gl.grade(improved_schedule, streets, intersections, paths, total_duration, bonus_points)
        print(new_score)
        if new_score > best_score:
            best_schedule = deepcopy(improved_schedule)
            best_score = new_score

        # Update the current solution with the best solution found so far.
        current_schedule = deepcopy(best_schedule)
    
    return best_schedule, best_score

file = input("Enter name of the input file, e.g. \"a.txt\": ")
start = time()
total_duration, bonus_points, intersections, streets, name_to_i_street, paths = gl.readInput(file)
schedule, score = ILS(streets, intersections, paths, total_duration, bonus_points, start, max_iterations=100)
time_spend = time() - start
gl.printSchedule(schedule, streets)
print("Score: ", score)
print("Time: ", time_spend)

output_file = "./outputs//" + file + ".output.txt"  # You can change the file name as needed
# Save the best schedule to a file.
gl.saveScheduleToFile(schedule, streets, output_file)
