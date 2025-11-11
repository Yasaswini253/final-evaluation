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

