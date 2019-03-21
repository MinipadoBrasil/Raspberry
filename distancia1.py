# Bibliotecas
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json
import serial
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np



# Modos do GPIO (Board/ BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO_TRIGGER = 18
GPIO_ECHO = 24

# Setar I/O do GPIO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)
#time.sleep(2)


def distance():

    #set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    #set Trigger after 0.01 ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    pulse_start = time.time()
    pulse_end = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()

    # time difference between start and arrival
    pulse_time = pulse_end - pulse_start
    #multiply with the sonic speed (34300 cm/s)
    distance = round(pulse_time * 17150,2)

    return distance

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
        try:
            tempo += 0.8
            tempo = round(tempo,0)
            dist = distance()
            print("Distância = %.1f cm \n" % dist)
            print("Tempo = %.1f s \n" % tempo)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping Services...")
            break
        with open("Distance_Time.csv","a") as f:
            writer = csv.writer(f, delimiter = ",")
            writer.writerow([tempo,dist])
        y_var = np.append(y_var,dist)
        x_var = np.append(x_var,tempo)
        y_var = y_var[1:plot_window+1]
        x_var = x_var[1:plot_window+1]
        fig.suptitle('Gráfico da Distancia [ºC] em função do Tempo [s]')
        ax.set_xlabel('Tempo [s]')
        ax.set_ylabel('Distancia [ºC]')
        line.set_ydata(y_var)
        line.set_xdata(x_var)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    #reset by pressing CRTL-C
    except KeyboardInterrupt:
        break

GPIO.cleanup()

