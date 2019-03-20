import serial
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('/dev/ttyACM1')
ser.flushInput()

plot_window = 20
y_var = np.array(np.zeros([plot_window]))
x_var = np.array(np.zeros([plot_window]))
plt.ion()
fig = plt.figure(figsize=(8,6))
ax = plt.subplot()
line, = ax.plot(y_var,'b.')
i = 0
tempo = 0
while True:
    try:
        if i%5 == 0:
            ser_bytes = ser.readline()
            try:
                tempo = round(tempo,1)
                decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                temperature = decoded_bytes
                print("Temperatura = ",temperature)
                print("Tempo =", tempo)
            except:
                continue
            with open("Storage_Data.csv","a") as f:
                writer = csv.writer(f, delimiter = ",")
                writer.writerow([tempo,temperature])
            y_var = np.append(y_var,temperature)
            x_var = np.append(x_var,tempo)
            y_var = y_var[1:plot_window+1]
            x_var = x_var[1:plot_window+1]
            fig.suptitle('Gráfico da Temperatura [ºC] em função do Tempo [s]')
            ax.set_xlabel('Tempo [s]')
            ax.set_ylabel('Temperatura [ºC]')
            line.set_ydata(y_var)
            line.set_xdata(x_var)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
        tempo += 1.0
        time.sleep(1.0)
        i += 1
    except KeyboardInterrupt:
        print("Stopping Services ...")
        
