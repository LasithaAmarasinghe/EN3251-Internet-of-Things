from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import json
import time

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\n")
    else:
        print("Connection failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client(mqtt_client.CallbackAPIVersion.VERSION1,"PythonPub")

# Set the callback function
client.on_connect = on_connect

broker_address = "test.mosquitto.org"  # broker's address
broker_port = 1883
keepalive = 5
qos = 1
publish_topic = "oranges"

# Connect to the MQTT broker
client.connect(broker_address, broker_port, keepalive)

# Start the MQTT loop to handle network traffic
client.loop_start()

# Publish loop

read_file_name = "data.json"
with open(read_file_name) as json_file:
            sensor_out= json.load(json_file)

print ("sensor_out is a ", type(sensor_out))
data_out=json.dumps(sensor_out)

# Data to send (JSON format)
# data = {
#     "device_id": "sensor_001",
#     "timestamp": "2024-09-12T10:00:00Z",
#     "temperature": 22.5,
#     "humidity": 55
# }

# json_payload = json.dumps(data)

try:
    while True:
        # Publish a message to the send topic
        
        #value = input('Enter the message: ')
        client.publish(publish_topic,data_out,qos)
        print(f"Published message '{data_out}' to topic '{publish_topic}'\n")
        
        # Wait for a moment to simulate some client activity
        time.sleep(6)

except KeyboardInterrupt:
    # Disconnect from the MQTT broker
    pass
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")

