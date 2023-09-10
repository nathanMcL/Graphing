# Pie Graph
# The purpose of this program:
# Prompt to enter a name for each label (QT One, QT Two)
# Prompt to enter numerical value (e.g., 2.33 or 7)
# Prompt to enter color (e.g., blue, red, #FF0000)

import matplotlib.pyplot as plt
import numpy as np
from tkinter import Tk, Label, Button, Entry, StringVar, END


class PieChartApp:
    def __init__(self, root):
        self.root = root
        root.title("My Pie Chart")
        root.geometry("400x600")  # Set the window size
        root.configure(bg="light grey")  # Set background color to light grey

        self.labels = []
        self.values = []
        self.colors = []
        self.data_labels = []  # List to keep track of the Tkinter labels

        self.label_text = StringVar()
        self.value_text = StringVar()
        self.color_text = StringVar()

        self.label_label = Label(root, text="Label", bg="light grey")
        self.label_label.pack()
        self.label_entry = Entry(root, textvariable=self.label_text)
        self.label_entry.pack()

        self.value_label = Label(root, text="Numerical Value", bg="light grey")
        self.value_label.pack()
        self.value_entry = Entry(root, textvariable=self.value_text)
        self.value_entry.pack()

        self.color_label = Label(root, text="Color", bg="light grey")
        self.color_label.pack()
        self.color_entry = Entry(root, textvariable=self.color_text)
        self.color_entry.pack()

        self.add_button = Button(root, text="Add", command=self.add_data)
        self.add_button.pack()

        self.plot_button = Button(root, text="Plot", command=self.plot_chart)
        self.plot_button.pack()

    def add_data(self):
        label = self.label_text.get()
        try:
            value = float(self.value_text.get())
            color = self.color_text.get()

            self.labels.append(label)
            self.values.append(value)
            self.colors.append(color)

            # Create a new Tkinter label to display this data
            data_label = Label(self.root, text=f"Label: {label}, Value: {value}, Color: {color}", bg="light grey")
            data_label.pack()
            self.data_labels.append(data_label)  # Keep track of the Tkinter label

            self.label_entry.delete(0, END)
            self.value_entry.delete(0, END)
            self.color_entry.delete(0, END)

        except ValueError:
            print("Please enter a valid numerical value.")

    def plot_chart(self):
        if len(self.values) == 0:
            print("No data to plot.")
            return

        plt.style.use('_mpl-gallery-nogrid')

        fig, ax = plt.subplots()
        ax.pie(self.values, labels=self.labels, colors=self.colors, radius=3, center=(4, 4),
               wedgeprops={"linewidth": 1, "edgecolor": "white"}, autopct='%1.1f%%', startangle=140)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
               ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()


if __name__ == "__main__":
    root = Tk()
    app = PieChartApp(root)
    root.mainloop()
