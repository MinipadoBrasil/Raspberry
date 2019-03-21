# Bibliotecas
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import json

#connecting to broker
broker_address = "192.168.4.145"
client = mqtt.Client("Programa da Distância")
print("connecting to broker")
client.connect(broker_address)

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
        #print("teste")
        pulse_start = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()

    # time difference between start and arrival
    pulse_time = pulse_end - pulse_start
    #multiply with the sonic speed (34300 cm/s)
    distance = round(pulse_time * 17150,2)

    return distance + 1.5

tempo = 0
try:
    while True:
        client.loop_start()
        tempo += 0.8
        tempo = round(tempo,0)
        dist = distance()
        teste = {'Dist':dist}
        #dados = {'time':tempo,'dist':dist}
        data_out = json.dumps(teste)
        #print("Subscribing to topic", "topic")
        client.subscribe("ultrasonic")
        #print("Publishing to topic", "topic")
        client.publish("ultrasonic", data_out)
        print("Distância = %.1f cm \n" % dist)
        print("Tempo = %.1f s \n" % tempo)
        time.sleep(1)
        client.loop_stop()
        
#reset by pressing CRTL-C
except KeyboardInterrupt:
    print("Stopping Services...")

finally:
    print("CLeaning  UP")
    GPIO.cleanup()
