import tkinter as tk
import serial
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =============================
# Serial Port Setup
# =============================
try:
    esp32 = serial.Serial('COM24', 9600, timeout=1)  # change COM6 to your port
    time.sleep(3)
    print("✅ ESP32 connected successfully.")
except Exception as e:
    esp32 = None
    print("❌ Could not connect to ESP32:", e)

# =============================
# Tkinter Setup
# =============================
root = tk.Tk()
root.title("ESP32 DHT11 Live Plot")
root.geometry("700x500")
root.configure(bg="#eef6fd")
<<<<<<< HEAD
=======
# Labels
tk.Label(root, text="Temperature (°C):", font=("Arial", 14), bg="#eef6fd").pack()
temp_label = tk.Label(root, text="-- °C", font=("Arial", 18, "bold"), fg="red", bg="#eef6fd")
temp_label.pack()

tk.Label(root, text="Humidity (%):", font=("Arial", 14), bg="#eef6fd").pack()
hum_label = tk.Label(root, text="-- %", font=("Arial", 18, "bold"), fg="blue", bg="#eef6fd")
hum_label.pack()

# =============================
# Matplotlib Setup
# =============================
fig = Figure(figsize=(5.5, 3), dpi=100)
ax = fig.add_subplot(111)
ax.set_title("DHT11 Live Readings")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Value")
ax.grid(True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=15)

time_data, temp_data, hum_data = [], [], []
start_time = time.time()
# =============================
# Data Update Function
# =============================
def update_data():
    global time_data, temp_data, hum_data

    if esp32 and esp32.in_waiting:
        raw = esp32.readline()
        line = raw.decode('utf-8', errors='ignore').strip()

