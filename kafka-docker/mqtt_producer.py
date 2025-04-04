import paho.mqtt.client as mqtt
from random import randrange, uniform
import time


# MQTT Broker details
mqttBroker = "25.27.63.155" 
port = 1883 
username = "mateo" 
password = "P@ssword!" 

# Topic to publish to
mqtt_topic = "application/2e54b59e-e89a-44b9-839d-488d610816a2/device/24e124743c407339/event/up"
# Client setup
mqtt_client = mqtt.Client("MQTTProducer1")  
# Set username and password
mqtt_client.username_pw_set(username, password)

mqtt_client.connect(mqttBroker, port)
    
while True:
    randomNumber = uniform(20.0, 21.0)
    mqtt_client.publish(mqtt_topic, randomNumber)
    print(f"MQTT: Just published {randomNumber} to topic {mqtt_topic}")
    time.sleep(3)