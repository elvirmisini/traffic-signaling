import re

import pandas as pd


def read_nohup_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

n = 'rezultati_12'

file_path = f'{n}.out'

raw_data = read_nohup_file(file_path)

pattern_instance = re.compile(r"The solution of (\S+\.txt) has the score (\d+).")
matches_instance = pattern_instance.findall(raw_data)

results_dict = {}

for match in matches_instance:
    instance, score = match
    instance_name = instance.replace(".txt", "")
    score = int(score)
    if instance_name not in results_dict:
        results_dict[instance_name] = []
    results_dict[instance_name].append(score)

summary_data = []

for instance_name, scores in results_dict.items():
    best_result = max(scores)
    average_result = sum(scores) / len(scores)
    summary_data.append([instance_name, best_result, average_result])

summary_df = pd.DataFrame(summary_data, columns=["Instance Name", "Best Result", "Average Result"])

instance_order = [
    "I7073_S9102_C1000",
    "I10000_S35030_C1000",
    "I8000_S95928_C1000",
    "I500_S998_C1000",
    "I1662_S10000_C1000",
    "I80_S240_C300",
    "I80_S480_C600",
    "I99_S399_C400",
    "I100_S500_C500",
    "I100_S600_C153",
    "I120_S480_C500",
    "I200_S1000_C400",
    "I220_S660_C430",
    "I300_S1500_C469",
    "I600_S3000_C332",
    "I2000_S12000_C57",
    "I3333_S13332_C428",
    "I4000_S24000_C401",
    "I9000_S36000_C1500",
    "I12000_S36000_C2000"
]

summary_df_filtered = summary_df[summary_df["Instance Name"].isin(instance_order)]
summary_df_filtered["Instance Name"] = pd.Categorical(summary_df_filtered["Instance Name"], categories=instance_order,
                                                      ordered=True)
summary_df_filtered = summary_df_filtered.sort_values("Instance Name")

print(len(summary_df_filtered))

summary_df_filtered.to_csv(f"{n}.csv", index=False)
