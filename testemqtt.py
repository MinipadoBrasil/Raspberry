import paho.mqtt.client as mqtt
import time

def on_message(client,userdata, message):
    print("Message received ",str(message.payload.decode("utf-8")))
    print("Message topic ", message.topic)
    print("Message qos ", message.qos)
    print("Message retain flag= ", message.retain)

broker_address = "192.168.4.145"
print("Creating new instance")
client = mqtt.Client("P1")
client.on_message = on_message
print("connecting to broker")
client.connect(broker_address)
client.loop_start()
print("Subscribing to topic", "topic")
client.subscribe("topic")
print("Publishing to topic", "topic")
client.publish("topic", "Oi")
time.sleep(4)
client.loop_stop()
