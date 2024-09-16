from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time
import os
from dotenv import load_dotenv


# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
        client.subscribe("Sensor_1",qos)
        client.subscribe("Water_level",qos)
    else:
        print("Connection failed with code {rc}")

def on_message(client, userdata, msg):
    global sensor_data
    global water_level
    topic = msg.topic
    if topic == "Sensor_1":
        sensor_data = str(msg.payload.decode("utf-8"))
    elif topic == "Water_level":
        water_level = str(msg.payload.decode("utf-8"))
    else:
        print("Unknown topic")

# Create an MQTT client instance
client = mqtt.Client(client_id="controller", clean_session=True)


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
sensor_data = "High"
water_level = "High"

try:
    while True:
       if sensor_data == "Low":
           if water_level == "Low":
               print("Water level is low, please refill the tank")
               client.publish("Dashboard","Water level is low, please refill the tank",qos)
           else:
                print("Water level is normal.Water Pump Started")
                client.publish("Dashboard","Water level is normal.Water Pump Started",qos)
                client.publish("Pump","Start",qos)
       if sensor_data == "High":
            print("Moisture level is high, Water Pump Stopped")
            client.publish("Dashboard","Moisture level is high, Water Pump Stopped",qos) 
            client.publish("Pump","Stop",qos)
    
       time.sleep(3)





except KeyboardInterrupt:
    # Disconnect from the MQTT broker
    pass
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")