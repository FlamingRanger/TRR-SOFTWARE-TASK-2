import tkinter as tk
from tkinter import ttk
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

class SensorGUI:
    def __init__(self, root):
        self.root = root
        self.ser = serial.Serial('COM3', 115200)  # Update COM port
        self.data = deque(maxlen=100)
        self.threshold = 512
        
        # GUI Setup
        self.root.title("Arduino Sensor Monitor")
        
        # Numerical Display
        self.value_label = ttk.Label(root, text="Value: 0", font=('Arial', 24))
        self.value_label.pack(pady=10)
        
        # Threshold Controls
        self.threshold_frame = ttk.Frame(root)
        self.threshold_frame.pack(pady=5)
        
        ttk.Label(self.threshold_frame, text="Threshold:").pack(side=tk.LEFT)
        self.threshold_entry = ttk.Entry(self.threshold_frame, width=8)
        self.threshold_entry.insert(0, str(self.threshold))
        self.threshold_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.threshold_frame, text="Set", 
                 command=self.update_threshold).pack(side=tk.LEFT)
        
        # Plot Setup
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.line, = self.ax.plot([], [])
        self.ax.set_ylim(0, 1023)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Reset Button
        ttk.Button(root, text="Reset", command=self.reset).pack(pady=10)
        
        # Start updates
        self.update()

    def update(self):
        try:
            raw = self.ser.readline().decode().strip()
            value = int(raw)
            self.data.append(value)
            
            # Update display
            self.value_label.config(
                text=f"Value: {value}",
                foreground="red" if value > self.threshold else "black"
            )
            
            # Update plot
            self.line.set_data(range(len(self.data)), self.data)
            self.ax.set_xlim(0, len(self.data))
            self.canvas.draw()
            
        except (ValueError, UnicodeDecodeError):
            pass
            
        self.root.after(50, self.update)

    def update_threshold(self):
        try:
            self.threshold = int(self.threshold_entry.get())
        except ValueError:
            pass

    def reset(self):
        self.data.clear()
        self.line.set_data([], [])
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorGUI(root)
    root.mainloop()
