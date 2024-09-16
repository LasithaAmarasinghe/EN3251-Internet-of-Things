from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time
import os
from dotenv import load_dotenv
import random

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
    else:
        print("Connection failed with code {rc}")


# Create an MQTT client instance
client = mqtt.Client(client_id="Sensor", clean_session=True)


# Set the callback function
client.on_connect = on_connect

#We are using our own broker(Mosquitto) hosted on a server
broker_address = "137.184.9.146"  # broker's address
broker_port = 1883
keepalive = 5
qos = 1


publish_topic = "Sensor_1"


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

def check_level():
    level = random.choice(["High", "Low"])
    print(f"Moisture level is {level}")
    return level


while True:
    moisture = check_level()
    client.publish(publish_topic,moisture,qos)#publish the moisture level
    time.sleep(3)#wait for 3 seconds







