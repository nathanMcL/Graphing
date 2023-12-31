# The purpose of this program:
# Plot given positive and negative values
# Create a line graph for the positive and negative values
# Assigned dates to plotted points
# Created off/on toggle for the line graphs click the [x]
# Added a notification once lines are toggled
# Created a hover text tooltip that displays current data

import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Button

# Data
values = [3.46, 4.23, 5.12, 6.45, 7.67, 8.76]
neg_values = [-.75, -1.25, -2.34, -2.11, -1.72]
dates = ["01/2023", "02/2023", "03/2023", "04/2023", "05/2023", "06/2023"]

# Generate x-coordinates for the values
x_values = [x * 2 for x in range(len(values))]

# Generate x-coordinates for the neg_values
x_neg_values = [(x * 2) + 1 for x in range(len(neg_values))]

# Create a figure and axes
fig, ax = plt.subplots()

# Scatter plot for positive and negative values
scatter1 = ax.scatter(x_values, values, c='green', label='Positive Values')
scatter2 = ax.scatter(x_neg_values, neg_values, c='red', label='Negative Values')

# Line plot to connect the positive and negative values
line1, = ax.plot(x_values, values, c='blue', label='Positive Line')
line2, = ax.plot(x_neg_values, neg_values, c='orange', label='Negative Line')

# Configure x-axis labels
xticks = x_values + x_neg_values
xticks.sort()
xticklabels = [dates[i // 2] if i % 2 == 0 else str(i) for i in xticks]
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

# Set axis labels and title
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_title('Matplotlib Graph with Toggle Buttons')

# Add legend
ax.legend()

# Add grid lines
ax.grid(True)


# Function to toggle lines when check buttons are clicked
def toggle_lines(label):
    if label == 'Positive Line':
        line1.set_visible(not line1.get_visible())
    elif label == 'Negative Line':
        line2.set_visible(not line2.get_visible())
    ax.set_title(f"{label} Toggled")
    plt.draw()


# Create check buttons to toggle lines
rax = plt.axes([0.8, 0.05, 0.15, 0.15])
labels = ['Positive Line', 'Negative Line']
check = CheckButtons(rax, labels, [True, True])

# Register the toggle function
check.on_clicked(toggle_lines)

tooltip = ax.annotate(
    "", xy=(0, 0), xytext=(20, 20),
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="w"),
    arrowprops=dict(arrowstyle="->")
)
tooltip.set_visible(False)


def on_hover(event):
    cont1, ind1 = scatter1.contains(event)
    cont2, ind2 = scatter2.contains(event)
    if cont1:
        ind = ind1["ind"][0]  # Take the first index from the array
        tooltip.xy = (event.xdata, event.ydata)
        tooltip.set_text(f"Positive: {values[ind]}")
        tooltip.set_visible(True)
    elif cont2:
        ind = ind2["ind"][0]  # Take the first index from the array
        tooltip.xy = (event.xdata, event.ydata)
        tooltip.set_text(f"Negative: {neg_values[ind]}")
        tooltip.set_visible(True)
    else:
        tooltip.set_visible(False)
    fig.canvas.draw_idle()


fig.canvas.mpl_connect('motion_notify_event', on_hover)

plt.show()
