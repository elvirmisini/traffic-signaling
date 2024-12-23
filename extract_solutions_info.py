import os

import pandas as pd

data = []

for file_name in os.listdir('output'):
    file_name_parts = file_name.split('_')

    instance_name = '_'.join(file_name_parts[0:3]).replace('.txt', '')
    variant = file_name_parts[4]
    version = file_name_parts[6]
    ils_iterations = file_name_parts[9]
    hill_climbing_iterations = file_name_parts[12]
    best_solution_time = file_name_parts[-4].split('.')[0]
    best_score = file_name_parts[-1].split('.')[0]

    data.append({
        'Instance Name': instance_name,
        'Variant': variant,
        'Version': version,
        'Nr ILS Iterations': ils_iterations,
        'Nr Hill Climbing Iterations': hill_climbing_iterations,
        'Best Solution Time': best_solution_time,
        'Best Score': best_score
    })

df = pd.DataFrame(data)

sorted_df = df.sort_values(by=['Instance Name', 'Variant', 'Version'])

output_csv = 'result_stats.csv'
sorted_df.to_csv(output_csv, index=False)
