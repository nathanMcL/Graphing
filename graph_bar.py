# Bar Graph
# Purpose of this program:
# providing a $value, display in succession
# Display the Calculated differance between each price point
# Depending on price values, colors will change to highlight positive/negative growth

import matplotlib.pyplot as plt
import mplcursors

# Data
labels = ['Jan/Feb', 'Apr/May', 'Jun/Jul', 'Aug/Sep', 'Oct/Nov', 'Dec']
prices = [1.25, 1.75, 2.21, 3.13, 4.32, 5.15]

# Determine colors based on prices
colors = []
for price in prices:
    if price < 3:
        colors.append('red')
    elif 3.01 <= price <= 4:
        colors.append('orange')
    else:
        colors.append('green')

errors = [0.05, 0.1, 0.08, 0.12, 0.15, 0.1]  # example error data

# Create bar chart
fig, ax = plt.subplots()
bars = ax.bar(labels, prices, color=colors, yerr=errors, capsize=5)

# Add Data Labels and Percentage Differences
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords='offset points',
                ha='center', va='bottom')

    if i > 0:
        percentage_diff = ((prices[i] - prices[i - 1]) / prices[i - 1]) * 100
        ax.annotate(f'{percentage_diff:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height / 2),
                    xytext=(0, 0),
                    textcoords='offset points',
                    ha='center', va='center',
                    fontsize=10, color='white')

# Add Legend
ax.legend(bars, labels, title='Months')

# Add Grid Lines
ax.grid(True, linestyle='--')

# Change background color to grey
ax.set_facecolor("lightgrey")
fig.patch.set_facecolor("lightgrey")

# Labeling
ax.set_xlabel('Months')
ax.set_ylabel('Price in $')
ax.set_title('Bar Graph')

# Interactivity
mplcursors.cursor(hover=True)

# Save plot
plt.savefig("Dynamic_Color_Bar_Graph.png")

# Show plots
plt.show()
