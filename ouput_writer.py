import os.path

SOLUTION_REPORTER_DIR = 'solution_reporter'
DATA_DIR = 'data'


def save_schedule_to_file(schedules, streets, filename) -> None:
    output_path = os.path.join(SOLUTION_REPORTER_DIR, DATA_DIR, filename + '.out.txt')

    with open(output_path, 'w') as file:
        file.write(str(len(schedules)) + '\n')
        for schedule in schedules:
            file.write(str(schedule.i_intersection) + '\n')
            file.write(str(len(schedule.order)) + '\n')
            for i in range(len(schedule.order)):
                line = streets[schedule.order[i]].name + ' ' + str(schedule.green_times[schedule.order[i]]) + '\n'
                file.write(line)
