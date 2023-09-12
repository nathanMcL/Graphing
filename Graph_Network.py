# The purpose of this program:
# GUI Prompt to monitor the connection between the localhost and target host
# Input a .com

# Operation:
# On press start
# Network uptime in blue
# Network downtime plots coordinates, in red
# Network response time in green
# Network response time plots coordinates ranged between 0.026-1.0, in orange

# Press stop: stops graphing network
# Press reset: reset the graph to start again
# Press save: To Excel sheet ***error error error lol :) *** Needs more attention. Not sure how to fix atm.


import logging
import time
import tkinter as tk
from datetime import datetime
from threading import Thread
from tkinter import simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from ping3 import ping

# Tkinter setup
root = tk.Tk()
root.withdraw()
target_host = simpledialog.askstring("Input", "Please enter the target host (e.g. google.com):")

# Initialization
timestamps = []
uptimes = []
response_times = []
down_times = []
down_timestamps = []
filtered_response_times = []
filtered_timestamps = []

monitoring = [False]

# Logging setup
logging.basicConfig(filename='network.log', level=logging.INFO)


# Function to toggle monitoring
def toggle(event):
    monitoring[0] = not monitoring[0]


# Ping thread
def ping_thread():
    while True:
        if monitoring[0]:
            response_time = ping(target_host)
            is_up = 1 if response_time is not None else 0
            current_time = time.time()
            formatted_time = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')

            timestamps.append(formatted_time)
            uptimes.append(is_up)
            response_times.append(response_time if response_time else 0)

            if is_up == 0:
                down_times.append(0)
                down_timestamps.append(formatted_time)

            logging.info(f"{formatted_time}, {is_up}, {response_time}")
            time.sleep(10)
        else:
            time.sleep(1)


# Matplotlib setup
fig, ax = plt.subplots()
button_ax = plt.axes([0.8, 0.01, 0.1, 0.075])
button = Button(button_ax, 'Start')
button.on_clicked(toggle)


# Reset
def reset(event):
    global timestamps, uptimes, response_times, down_times, down_timestamps, filtered_response_times, filtered_timestamps
    timestamps = []
    uptimes = []
    response_times = []
    down_times = []
    down_timestamps = []
    filtered_response_times = []
    filtered_timestamps = []
    monitoring[0] = False
    plt.clf()  # Clear the current figure
    plt.ion()  # Enable interactive mode
    plt.grid(True)  # Show the grid


ax2 = ax.twinx()
plt.ion()
plt.grid(True)


# Save the data to Excel format
def save_to_excel(event):
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Uptime': uptimes,
        'Response Times': response_times,
        'Down Timestamps': down_timestamps,
        'Down Times': down_times,
        'Filtered Response Times': filtered_response_times,
        'Filtered Timestamps': filtered_timestamps
    })

    filename = f"network_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


# Start the ping thread
t = Thread(target=ping_thread)
t.daemon = True
t.start()

while True:
    if monitoring[0]:
        plt.clf()  # Clear figure to redraw
        ax = plt.gca()
        # Plotting logic here
        ax.plot(timestamps, uptimes, label='Uptime Status', color='blue')
        ax.scatter(down_timestamps, down_times, color='red', label='Down Times')

        ax2 = ax.twinx()
        ax2.plot(timestamps, response_times, label='Response Time (ms)', color='green')

        filtered_response_times = [t for t in response_times if 0.026 <= t <= 1.0]
        filtered_timestamps = [timestamps[i] for i, t in enumerate(response_times) if 0.026 <= t <= 1.0]
        ax2.scatter(filtered_timestamps, filtered_response_times, color='orange', label='Filtered Response Times')

        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')

        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel('Time')
        ax.set_ylabel('Is Up')
        ax2.set_ylabel('Response Time (ms)')

        button_ax = plt.axes([0.8, 0.01, 0.1, 0.075])
        button = Button(button_ax, 'Stop')
    else:
        ax = plt.gca()  # This ensures that the 'Start' button can be redrawn without clearing the figure
        # If not monitoring, add a 'Start' button
        button_ax = plt.axes([0.8, 0.01, 0.1, 0.075])
        button = Button(button_ax, 'Start/Stop')

    button.on_clicked(toggle)

    # Add Reset button
    reset_button_ax = plt.axes([0.7, 0.01, 0.1, 0.075])
    reset_button = Button(reset_button_ax, 'Reset')
    reset_button.on_clicked(reset)

    # Add save to "Excel" button
    save_button_ax = plt.axes([0.6, 0.01, 0.1, 0.075])
    save_button = Button(save_button_ax, 'Save')
    save_button.on_clicked(save_to_excel)

    plt.grid(True)
    plt.pause(1)
