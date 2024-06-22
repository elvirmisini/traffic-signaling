import matplotlib.pyplot as plt

# Data
selection_percentage = [10, 15, 20, 25, 30]
best_instances = [10, 6, 1, 2, 1]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(selection_percentage, best_instances, marker='o', linestyle='-', color='b')
plt.xlabel('Perqinja e selektimit te udhekryqeve (%)')
plt.ylabel('Numri i instancave me te mira')
# plt.title('Numri i instancave me te mira per Perqinja e selektimit te udhekryqeve')
plt.grid(True)
plt.show()
