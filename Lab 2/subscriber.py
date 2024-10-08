from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import json
import time

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(subscribe_topic,qos)  # Subscribe to the receive topic
    else:
        print("Connection failed with code {rc}")
write_file_name = "sensor_received.json"

# Callback when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    print ("Message received " + "on "+ subscribe_topic + ": "  + str(msg.payload.decode("utf-8")))
    recieved = str(msg.payload.decode("utf-8"))
    sensor_in=json.loads(recieved) #convert incoming JSON to object
    print ("recieved is a ", type(recieved))
    print ("\nHumidity = ", sensor_in["humidity"])
    with open(write_file_name, 'w') as json_file:
        json.dump(sensor_in, json_file, indent=4)  # The 'indent' parameter adds pretty formatting
        print("Data has been written to", write_file_name)

# Create an MQTT client instance
client = mqtt.Client(mqtt_client.CallbackAPIVersion.VERSION1,"PythonSub")

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
broker_address = "test.mosquitto.org"  # broker's address
broker_port = 1883
keepalive = 5
qos = 1

# subscribe_topic = input ('Enter the topic to subscribe to: ')
subscribe_topic = "oranges"
client.connect(broker_address, broker_port, keepalive)

# Start the MQTT loop to handle network traffic
client.loop_start()

# Subscribe loop

try:
    while True:
        time.sleep(6)

except KeyboardInterrupt:
    # Disconnect from the MQTT broker
    pass
client.loop_stop()
client.disconnect()

print("Disconnected from the MQTT broker")