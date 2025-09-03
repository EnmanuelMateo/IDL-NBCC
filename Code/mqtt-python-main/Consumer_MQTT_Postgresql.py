#!/usr/bin/env python3
import os, json, time, signal
from dotenv import load_dotenv
from confluent_kafka import Consumer
import psycopg2
from psycopg2.extras import Json

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC     = os.getenv("KAFKA_TOPIC", "sensor_data")

PG_CONFIG = dict(
    host=os.getenv("PGHOST", "localhost"),
    port=int(os.getenv("PGPORT", "5432")),
    dbname=os.getenv("PGDATABASE", "idl_data_warehouse_rdb"),
    user=os.getenv("PGUSER", "idl_iot"),
    password=os.getenv("PGPASSWORD", "")
)

C = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP,
    "group.id": "mqtt_consumer_group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False
})

running = True

DDL = """
CREATE TABLE IF NOT EXISTS mqtt_data (
  id SERIAL PRIMARY KEY,
  payload JSONB NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT now()
);
"""

def ensure_table():
    with psycopg2.connect(**PG_CONFIG) as conn, conn.cursor() as cur:
        cur.execute(DDL)
        conn.commit()

def insert_payload(obj):
    with psycopg2.connect(**PG_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO mqtt_data (payload) VALUES (%s);", (Json(obj),))
        conn.commit()

def shutdown(*_):
    global running
    running = False
    print("\n[Consumer] 🛑 Shutting down…")
    try:
        C.close()
    except Exception:
        pass

def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    ensure_table()

    print(f"[Kafka] 🔗 Connecting to {KAFKA_BOOTSTRAP} and subscribing to {KAFKA_TOPIC}")
    C.subscribe([KAFKA_TOPIC])

    while running:
        msg = C.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"[Kafka] ❌ {msg.error()}")
            continue
        try:
            raw = msg.value().decode("utf-8", errors="ignore")
            try:
                data = json.loads(raw)
            except Exception:
                data = {"raw": raw}
            insert_payload(data)
            C.commit(asynchronous=False)
            print(f"[Pipe] Kafka→Postgres | offset={msg.offset()}")
        except Exception as e:
            print(f"[Consumer] ❌ {e}")
            time.sleep(1)

    print("[Consumer] ✅ Exit.")

if __name__ == "__main__":
    main()
