import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time
import json

# MQTT Broker details
mqttBroker = "25.27.63.155"
port = 1883
username = "mateo"
password = "P@ssword!"

# Topic to publish to (MQTT)
mqtt_topic = "application/2e54b59e-e89a-44b9-839d-488d610816a2/device/24e124743c407339/event/up"

# Client setup (MQTT)
mqtt_client = mqtt.Client("MQTTBridge")
mqtt_client.username_pw_set(username, password)
mqtt_client.connect(mqttBroker, port)

#kafka set up
kafka_client = KafkaClient(hosts='kafka:9092') 
kafka_topic = kafka_client.topics['Sensor1']
kafka_producer = kafka_topic.get_sync_producer()

def on_message(client, userdata, message):
    try:
        print("Received MQTT message:", message.payload.decode("utf-8"))  # Added log
        json_data = json.loads(message.payload.decode("utf-8"))
        object_data = json_data["object"]
        time_data = json_data["time"]

        kafka_message = {
            "object": object_data,
            "time": time_data
        }
        kafka_producer.produce(json.dumps(kafka_message).encode('ascii'))
        print(f"Published to Kafka: {kafka_topic.name}, Message: {kafka_message}")  # Added log

    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing message: {e}")
        print(f"Raw message payload: {message.payload.decode('utf-8')}")

mqtt_client.loop_start()
mqtt_client.subscribe(mqtt_topic)
mqtt_client.on_message = on_message

while True:
    time.sleep(1)  # Prevent high CPU usage