#!/usr/bin/env python3
import os, json, time, signal, sys
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from confluent_kafka import Producer

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC     = os.getenv("KAFKA_TOPIC", "sensor_data")

MQTT_HOST  = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT  = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "idl/all_iot/idl_data")

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})
running = True

def delivery_report(err, msg):
    if err is not None:
        print(f"[Kafka] ❌ Delivery failed: {err}")
    else:
        print(f"[Kafka] ✅ Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] ✅ Connected to {MQTT_HOST}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] 📡 Subscribed: {MQTT_TOPIC}")
    else:
        print(f"[MQTT] ❌ Connect failed rc={rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors="ignore").strip()
    try:
        # If it’s JSON already, keep it; otherwise wrap it
        data = json.loads(payload) if (payload.startswith("{") or payload.startswith("[")) else {"value": payload}
        data["_meta"] = {
            "mqtt_topic": msg.topic,
            "ts": time.time()
        }
        producer.produce(KAFKA_TOPIC, value=json.dumps(data), key=str(time.time()), callback=delivery_report)
        producer.poll(0)
        print(f"[Pipe] MQTT→Kafka | topic={msg.topic} -> {KAFKA_TOPIC}")
    except Exception as e:
        print(f"[Producer] ❌ Error processing message: {e}")

def shutdown(*_):
    global running
    running = False
    print("\n[Producer] 🛑 Shutting down…")
    try:
        producer.flush(10)
    except Exception:
        pass

def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    while running:
        try:
            print(f"[MQTT] 🔌 Connecting to {MQTT_HOST}:{MQTT_PORT} …")
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            client.loop_start()
            while running:
                time.sleep(1)
            break
        except Exception as e:
            print(f"[MQTT] ❌ Connect error: {e} (retrying in 5s)")
            time.sleep(5)

    client.loop_stop()
    client.disconnect()
    print("[Producer] ✅ Exit.")

if __name__ == "__main__":
    main()
