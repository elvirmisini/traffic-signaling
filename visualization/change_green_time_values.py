import pandas as pd
import matplotlib.pyplot as plt

# Data
data = {
    "Instance": [
        "I70_S210_C200", "I99_S399_C400", "I100_S600_C153", "I101_S610_C154",
        "I102_S620_C155", "I103_S630_C156", "I104_S640_C157", "I105_S650_C158",
        "I106_S660_C159", "I107_S670_C160"
    ],
    "Positive & Negative": [
        69579, 145621, 308859, 140682, 486105, 139358, 684555, 54493, 103043, 1573953
    ],
    "Positive Only": [
        69535, 145465, 308770, 140669, 486047, 139317, 684817, 54484, 103014, 1571622
    ],
    "Negative Only": [
        69510, 145451, 308744, 140704, 486065, 139310, 684900, 54486, 103013, 1571622
    ]
}

df = pd.DataFrame(data)

# Calculate the mean for each instance across the strategies
means = df[['Positive & Negative', 'Positive Only', 'Negative Only']].mean(axis=1)

# Subtract mean from each strategy to find deviation
df['Pos&Neg Deviation'] = df['Positive & Negative'] - means
df['Pos Only Deviation'] = df['Positive Only'] - means
df['Neg Only Deviation'] = df['Negative Only'] - means

# Plotting the deviations
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(df['Instance'], df['Pos&Neg Deviation'], marker='o', label='Positive & Negative Deviation')
ax.plot(df['Instance'], df['Pos Only Deviation'], marker='o', label='Positive Only Deviation')
ax.plot(df['Instance'], df['Neg Only Deviation'], marker='o', label='Negative Only Deviation')

# Setting labels and title
ax.set_xlabel('Instance')
ax.set_ylabel('Deviation')
ax.set_title('Deviation from Mean Strategy Value by Instance')
ax.set_xticks(range(len(df['Instance'])))  # Set the ticks to be the instances
ax.set_xticklabels(df['Instance'], rotation=90)  # Rotate the instance labels for better visibility

# Adding a legend
ax.legend()

# Showing the plot
plt.grid(True)
plt.tight_layout()  # Adjust layout
plt.show()
