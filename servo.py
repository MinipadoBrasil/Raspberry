#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt
import signal
from pyfirmata import Arduino, util
board = Arduino('/dev/ttyACM0')
it = util.Iterator(board)
it.start()
servo1 = board.get_pin('d:3:s')
servo2 = board.get_pin('d:10:s')


def ResetBall():
    reset = int(input("Iniciar:1\n Parar:2\nResetar: 3\nNada:4\nEscolha: "))
    #reset = msg.payload.decode()
    if reset == 1:
        servo2.write(40)
    if reset == 2:
        servo2.write(140)
    if reset == 3:
        Angle = servo1.read()
        servo2.write(40)
        for x in range(Angle, 0,-1):
            servo1.write(x-1)
            time.sleep(0.1)
        servo2.write(140)
        time.sleep(2)
        for x in range(0, 30, 1):
            servo1.write(x+1)
            time.sleep(0.1)
    if reset == 4:
        pass


servo1.write(0)
print(servo2.read())
ref = servo1.read()
if ref < 15:
    for x in range(ref,15,+1):
        servo1.write(x+1)
        time.sleep(0.1)
    ref = 15
else:
    for x in range(ref,15,-1) :
        servo1.write(x-1)
        time.sleep(0.1)
    ref = 15
try:
    while True:
        Angle = int(input("Digite o angulo que você deseja: ")) + 15
        ref = servo1.read()
        time.sleep(0.1)
        if (Angle >= 15 and Angle <= 105):
            if (Angle > ref):
                for x in range(ref,Angle,+1):
                    servo1.write(x+1)
                    time.sleep(0.1)
                ref = Angle
            else:
                for x in range(ref,Angle,-1):
                    servo1.write(x-1)
                    time.sleep(0.1)
                ref = Angle
            print("Angulo = ", Angle - 15
        ResetBall()
        
except KeyboardInterrupt:
    print("\n Stopping Services...")
    servo2.write(70)
    Angle = servo1.read()
    for x in range(Angle, 0,-1):
        servo1.write(x-1)
        time.sleep(0.1)
        if x == 1:
            break





##client = mqtt.Client()
##client.connect("localhost",port=1883, keepalive=60, bind_address="")
##port = 8080
##usr = ''
##pwd = ''
##client_id = "client_id_4"
