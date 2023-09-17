# The purpose of this program:
# Graph the cpu data usage
# Graph the ram data usage
# Graph the network speed

import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import psutil
import threading
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt

# Initialize global variables to store CPU, RAM, and network speed data
cpu_data = [0] * 10
ram_data = [0] * 10
net_speed_data = [0] * 10
is_running = True  # Flag to control data collection


# Function to toggle data collection
def toggle_running():
    global is_running
    is_running = not is_running


# Function to save the graph as a PNG file
def save_graph():
    fig.savefig('system_monitoring_data.png')


# Function to update system information and graph
def update_system_info():
    global cpu_data, ram_data, net_speed_data
    cpu_scale_factor = 10  # Scale CPU data by this factor
    ram_scale_factor = 10  # Scale RAM data by this factor

    prev_net_info = psutil.net_io_counters()
    while True:
        if is_running:
            # Collect CPU, RAM and Network usage data
            cpu_usage = psutil.cpu_percent(interval=1) * cpu_scale_factor
            ram = psutil.virtual_memory()
            ram_percent = ram.percent * ram_scale_factor
            net_info = psutil.net_io_counters()
            net_speed = net_info.bytes_recv - prev_net_info.bytes_recv

            # Define sent and received here
            sent = net_info.bytes_sent
            received = net_info.bytes_recv

            # Set text labels
            cpu_var.set(f"CPU Usage: {cpu_usage / cpu_scale_factor}%")  # Revert scaling for display
            ram_var.set(f"RAM Usage: {ram_percent / ram_scale_factor}%")  # Revert scaling for display
            network_var.set(f"Data Sent: {sent} Bytes\nData Received: {received} Bytes\nNetwork Speed: {net_speed} B/s")

            # Append new data and remove old data if necessary
            cpu_data.append(cpu_usage)
            ram_data.append(ram_percent)
            net_speed_data.append(net_speed)

            for data in [cpu_data, ram_data, net_speed_data]:
                if len(data) > 10:
                    del data[0]

            # Update graph
            line_cpu.set_ydata(cpu_data)
            line_ram.set_ydata(ram_data)
            line_net_speed.set_ydata(net_speed_data)

            # Update y-axis limits dynamically
            ax1.set_ylim(min(cpu_data), max(cpu_data))
            ax2.set_ylim(min(ram_data), max(ram_data))
            ax3.set_ylim(min(net_speed_data), max(net_speed_data))

            # Update x-axis dynamically
            ax1.set_xlim(left=max(0, len(cpu_data) - 10), right=len(cpu_data))
            ax2.set_xlim(left=max(0, len(cpu_data) - 10), right=len(cpu_data))
            ax3.set_xlim(left=max(0, len(cpu_data) - 10), right=len(cpu_data))

            fig.canvas.draw_idle()
            prev_net_info = net_info

            root.update_idletasks()


# Enable zoom
def enable_zoom():
    canvas.toolbar.zoom()


# Enable pan
def enable_pan():
    canvas.toolbar.pan()


# Initialize GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("System Monitoring Tool")

# Initialize text variables for labels
cpu_var = tk.StringVar(value="CPU Usage:")
ram_var = tk.StringVar(value="RAM Usage:")
network_var = tk.StringVar(value="Data Sent:\nData Received:")

# Add labels and buttons to the GUI
ctk.CTkLabel(root, text="System Monitoring Tool", font=("Arial", 16)).pack(pady=10)
ctk.CTkLabel(root, textvariable=cpu_var).pack(pady=5)
ctk.CTkLabel(root, textvariable=ram_var).pack(pady=5)
ctk.CTkLabel(root, textvariable=network_var).pack(pady=5)

# Create Start and Stop buttons
start_stop_btn = ctk.CTkButton(root, text="Start/Stop", command=toggle_running)
start_stop_btn.pack(pady=5)

# Create Save button
save_btn = ctk.CTkButton(root, text="Save Graph", command=save_graph)
save_btn.pack(pady=5)

# Create a figure for the graph
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 12))
line_cpu, = ax1.plot(range(len(cpu_data)), cpu_data, label='CPU Usage', color='blue')
line_ram, = ax2.plot(range(len(ram_data)), ram_data, label='RAM Usage', color='red')
line_net_speed, = ax3.plot(range(len(net_speed_data)), net_speed_data, label='Net Speed', color='green')

# Place legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
ax3.legend(loc='upper left')

# Add grids to the subplots
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

# Embed the graph in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create Custom Toolbar
toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

zoom_btn = tk.Button(toolbar_frame, text="Zoom", command=enable_zoom)
zoom_btn.pack(side=tk.LEFT, padx=2, pady=2)

pan_btn = tk.Button(toolbar_frame, text="Pan", command=enable_pan)
pan_btn.pack(side=tk.LEFT, padx=2, pady=2)

# Add navigation toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

thread = threading.Thread(target=update_system_info, daemon=True)
thread.start()

root.mainloop()
