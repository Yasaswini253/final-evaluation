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

        if line:
            print("📡 Received:", line)
            try:
                t, h = map(float, line.split(','))
                temp_label.config(text=f"{t:.1f} °C")
                hum_label.config(text=f"{h:.1f} %")

                current_time = round(time.time() - start_time, 1)
                time_data.append(current_time)
                temp_data.append(t)
                hum_data.append(h)

                if len(time_data) > 30:
                    time_data = time_data[-30:]
                    temp_data = temp_data[-30:]
                    hum_data = hum_data[-30:]

                # Clear and replot
                ax.clear()
                ax.plot(time_data, temp_data, color='red', label='Temperature (°C)', marker='o')
                ax.plot(time_data, hum_data, color='blue', label='Humidity (%)', marker='x')
                ax.set_title("DHT11 Live Readings (ESP32)")
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Value")
                ax.legend(loc='upper right')
                ax.grid(True)
                canvas.draw()
            except ValueError:
                print("⚠️ Invalid line:", line)

    root.after(2000, update_data)

update_data()

# =============================
# Run GUI
# =============================
try:
    root.mainloop()
finally:
    if esp32:
        esp32.close()
        print("🔌 Serial closed.")
