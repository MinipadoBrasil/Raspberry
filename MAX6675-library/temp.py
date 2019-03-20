import serial
import time
import paho.mqtt.client as mqttClient
#ser = serial.Serial('/dev/ttyACM1')
#ser.flushInput()
#tempo = 0

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection Failed")

def on_message(client,userdata,message):
    print("Mensagem recebida", message.payload)


Connected = False
broker_adress = 'localhost'
port = 1883
user = ''
password = ''
client = mqttClient.client("teste")
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message
client.connect(broker_address, port=port)  #connect to broker
client.loop_start()                        #start the loop


while Connected != True:
    time.sleep(0.1)    

client.subscribe('teste')

try:
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Stopping Services ...")
    client.disconnect()
    client.loop_stop()
        
