from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time
import os
from dotenv import load_dotenv

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
        client.subscribe("Pump",qos)
    else:
        print("Connection failed with code {rc}")

def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    global pump
    if message == "Start":
        pump = "start"
    elif message == "Stop":
        pump = "stop"

# Create an MQTT client instance
client = mqtt.Client(client_id="pump", clean_session=True)


# Set the callback function
client.on_connect = on_connect
client.on_message = on_message

#We are using our own broker(Mosquitto) hosted on a server
broker_address = "137.184.9.146"  # broker's address
broker_port = 1883
keepalive = 5
qos = 1


load_dotenv()#load the environment variables
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']
client.username_pw_set(username, password)


# Connect to the MQTT broker
client.connect(broker_address, broker_port, keepalive)

# Start the MQTT loop to handle network traffic
client.loop_start()

# Publish loop
time.sleep(2)#wait for the connection to establish

def pump_start():
    print("Water Pump Started")
    
def pump_stop():
    print("Water Pump Stopped")




pump = "stop"
try:
    while True:
       time.sleep(3)
       if pump == "start":
            pump_start()
            pump = "stop"#reset the pump status in case of controller failure
       elif pump == "stop":
            pump_stop()

except KeyboardInterrupt:
    # Disconnect from the MQTT broker
    pass
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")