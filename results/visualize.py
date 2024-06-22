import matplotlib.pyplot as plt
import pandas as pd

# Data provided by the user
data = {
    'INSTANCA': [
        'B - BY THE OCEAN', 'C - CHECKMATE', 'D - DAILY COMMUTE', 'E- ETOILE', 'F- FOREVER JAMMED',
        'I80_S240_C300', 'I80_S480_C600', 'I99_S399_C400', 'I100_S500_C500', 'I100_S600_C153',
        'I120_S480_C500', 'I200_S1000_C400', 'I220_S660_C430', 'I300_S1500_C469', 'I600_S3000_C332',
        'I2000_S12000_C57', 'I3333_S13332_C428', 'I4000_S24000_C401', 'I9000_S36000_C1500', 'I12000_S36000_C2000'
    ],
    '200': [
        4566769, 1300636, 1588987, 746811, 1304770, 108240, 479753, 145738, 450112, 71664,
        568601, 19309, 129712, 589909, 122527, 54495, 103095, 1695834, 1128522, 2785071
    ],
    '400': [
        4566943, 1301264, 1594480, 748472, 1302362, 108259, 476911, 145777, 450152, 71761,
        568664, 19770, 132509, 590011, 122959, 54499, 103122, 1695873, 1128523, 2785092
    ],
    '600': [
        4566942, 1301442, 1593588, 746072, 1303514, 108277, 478395, 145816, 450207, 73744,
        568695, 20872, 135392, 590087, 122700, 54503, 103130, 1695864, 1128569, 2785109
    ],
    '800': [
        4567046, 1301796, 1595487, 744740, 1303074, 108270, 483527, 145826, 450259, 73878,
        568747, 20631, 138124, 590109, 122777, 54503, 103138, 1695875, 1128579, 2785116
    ],
    '1000': [
        4567054,
        1301830,
        1591469,
        748797,
        1306952,
        108277,
        482186,
        145824,
        450246,
        72488,
        568779,
        21355,
        136736,
        590168,
        123022,
        54506,
        103147,
        1695900,
        1128598,
        2785137
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

improvements = df.set_index('INSTANCA').apply(lambda x: x - x[0], axis=1).iloc[:, 1:]

# Plot the improvements
plt.figure(figsize=(20, 10))
for index, row in improvements.iterrows():
    plt.plot(improvements.columns, row, label=index, marker='o')

plt.title('Improvements in Objective Value with Increasing Inner Iterations')
plt.xlabel('Number of Inner Iterations')
plt.ylabel('Improvement in Objective Value')
plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
plt.grid(True)
plt.show()
