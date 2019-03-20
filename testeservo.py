#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt
import signal
from pyfirmata import Arduino, util
board = Arduino('/dev/ttyACM0')
it = util.Iterator(board)
it.start()
servo = board.get_pin('d:10:p')
servo.write(0)
time.sleep(1)
servo.write(90)
##client = mqtt.Client()
