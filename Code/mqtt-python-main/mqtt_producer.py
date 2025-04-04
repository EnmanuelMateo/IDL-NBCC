import paho.mqtt.client as mqtt
from random import randrange, uniform
import time


# MQTT Broker details
mqttBroker = "25.27.63.155"  # Replace with your broker's IP
port = 1883  # Default MQTT port
username = "mateo"  # username
password = "P@ssword!"  # password

# Topic to publish to
topic = "application/2e54b59e-e89a-44b9-839d-488d610816a2/device/24e124743c407339/event/up"

# Client setup
mqtt_client = mqtt.Client("MQTTProducer1")  
# Set username and password
mqtt_client.username_pw_set(username, password)

mqtt_client.connect(mqttBroker, port)

# Function to publish a message (you can customize this)
def publish_message(message):
    mqtt_client.publish(topic, message)
    print(f"Published '{message}' to topic '{topic}'")
    
while True:
    randomNumber = uniform(20.0, 21.0)
    mqtt_client.publish("Sensor1", randomNumber)
    print('MQTT: Just published ' + str(randomNumber) + ' to topic Sensor1')
    time.sleep(3)