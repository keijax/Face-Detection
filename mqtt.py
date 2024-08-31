from paho.mqtt import client as mqtt
import time
# Define the MQTT parameters
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 8080
CLIENT_NAME = "Bannana"
MQTT_TOPIC = "testmqttshaf"

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} {msg.payload.decode()}")

# Initialize the MQTT client
client = mqtt.Client(CLIENT_NAME, transport="websockets", protocol=mqtt.MQTTv311)

# Assign event callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT server
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Function to send a message
def send_message(message):
    client.publish(MQTT_TOPIC, message, qos=2)

def start(message_to_mobile="UNKOWN"):
    # Start the MQTT client
    client.loop_start()

    # Example of sending a message
    send_message(message_to_mobile)

    # Keep the script running to listen for messages
    try:
        while True:
            time.sleep(2)
            break
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        

