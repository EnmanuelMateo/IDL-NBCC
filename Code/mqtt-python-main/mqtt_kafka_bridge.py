import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time


# MQTT Broker details
mqttBroker = "25.27.63.155"  # Replace with your broker's IP
port = 1883  # Default MQTT port
username = "mateo"  # username
password = "P@ssword!"  # password

# Topic to publish to
topic = "application/2e54b59e-e89a-44b9-839d-488d610816a2/device/24e124743c407339/event/up"

# Client setup
mqtt_client = mqtt.Client("MQTTBridge")  
# Set username and password
mqtt_client.username_pw_set(username, password)

mqtt_client.connect(mqttBroker, port)


kafka_client = KafkaClient(hosts='localhost:9092')
kafka_topic = kafka_client.topics['Sensor1']
kafka_producer = kafka_topic.get_sync_producer()

def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    print('Received MQTT message', msg_payload)
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('KAFKA: Just published ' + str(msg_payload) + ' to topic Sensor1')
    

mqtt_client.loop_start()
mqtt_client.subscribe("TEMPERATURE")
mqtt_client.on_message = on_message
time.sleep(30)
mqtt_client.loop_stop()