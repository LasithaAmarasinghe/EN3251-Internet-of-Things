from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt
import time

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(subscribe_topic, qos)  # Subscribe to the receive topic
    else:
        print("Connection failed with code {rc}")

# Callback when a message is received from the subscribed topic
def on_message(client, userdata, msg):
    print("Message received " + "on " + subscribe_topic + ": " + str(msg.payload.decode("utf-8")))

# Create an MQTT client instance
client = mqtt.Client(mqtt_client.CallbackAPIVersion.VERSION1, "PythonSub")

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
broker_address = "test.mosquitto.org"  # broker's address
broker_port = 1883
keepalive = 5
qos = 1

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