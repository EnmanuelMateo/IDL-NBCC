import json
import logging
import psycopg2
from confluent_kafka import Consumer
from psycopg2.extras import Json

# PostgreSQL connection details
# DB_CONFIG = {
#     "dbname": "test",
#     "user": "postgres",
#     "password": "0273",
#     "host": "localhost",
#     "port": 5432
# }
DB_CONFIG = {
    "dbname": "idl_data_warehouse_rdb",
    "user": "idl_iot",
    "password": "IDL!2025IoT",
    "host": "vm-nbcc-wforecast-postgresql.at.remote.it",
    "port": 33003
}



# Connect to PostgreSQL
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mqtt_consumer_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['sensor_data'])  # Subscribe to MQTT-based Kafka topic

def categorize_device_type(device_type):
    device_type = device_type.lower()
    if "milesight ir people counter" in device_type or "people counter - ai tof" in device_type or "milesight tof people counter" in device_type:
        return "People_Counter"
    elif "people counter - ai wpo" in device_type:
        return "AI_People_Counter"
    elif "temperature & relative humidity" in device_type:
        return "Environmental_Monitoring"
    elif "illumination, temperature & relative humidity" in device_type:
        return "Multi_Sensor_Monitoring"
    elif "sound level" in device_type:
        return "Sound_Level_Monitoring"
    elif "ambience" in device_type:
        return "Ambience_Monitoring"
    else:
        return "Unknown_Devices"


def store_data(sensor_data):
    timestamp = sensor_data.get("timestamp", "Unknown")
    device_type = sensor_data.get("device_type", "Unknown Type")
    device_name = sensor_data.get("device_name", "Unknown Name")
    location = sensor_data.get("location", "Unknown Location")
    sublocation = sensor_data.get("sublocation", "Unknown Sublocation")
    sensor_readings = sensor_data.get("sensor_readings", [])

    table_name = categorize_device_type(device_type)

    battery_main = None
    battery_node = None
    total_in = None
    total_out = None
    period_in = None
    period_out = None
    temperature = None
    humidity = None
    illumination = None
    region_counts_1 = None
    region_counts_2 = None
    region_counts_3 = None
    region_counts_4 = None
    region_counts_5 = None
    region_counts_6 = None
    region_counts_7 = None
    region_counts_8 = None

    la_max = None
    la_eq = None
    la = None
    battery_voltage = None

    co2 = None
    hcho = None
    light_level = None
    pir_trigger = None
    pm10 = None
    pm2_5 = None
    pressure = None
    tvoc = None

    if isinstance(sensor_readings, list):
        for sensor in sensor_readings:
            sensor_name = sensor.get("sensor_name", "Unknown Sensor")
            sensor_data = sensor.get("sensor_reading_data", {})

            if "Battery Main Sensor" in sensor_name:
                battery_main = sensor_data["Battery_Main"]["value"]
            elif "Battery Node Sensor" in sensor_name:
                battery_node = sensor_data["Battery_Node"]["value"]
            elif "Battery Voltage Sensor" in sensor_name:
                battery_voltage = sensor_data["Battery_Voltage"]["value"]
            elif "Sound Level Sensor" in sensor_name:
                la_max = sensor_data["La_Max"]["value"]
                la_eq = sensor_data["La_Eq"]["value"]
                la = sensor_data["La"]["value"]
            elif "MS-AI Work Place" in sensor_name:
                region_counts_1 = sensor_data["Region_1_Count"]["value"]
                region_counts_2 = sensor_data["Region_2_Count"]["value"]
                region_counts_3 = sensor_data["Region_3_Count"]["value"]
                region_counts_4 = sensor_data["Region_4_Count"]["value"]
                region_counts_5 = sensor_data["Region_5_Count"]["value"]
                region_counts_6 = sensor_data["Region_6_Count"]["value"]
                region_counts_7 = sensor_data["Region_7_Count"]["value"]
                region_counts_8 = sensor_data["Region_8_Count"]["value"]
            elif "People Counting Sensor"  in sensor_name or "MS-AI ToF People Counting Sensor" in sensor_name:
                total_in = sensor_data.get("Total_in", {}).get("value")
                total_out = sensor_data.get("Total_out", {}).get("value")
                period_in = sensor_data.get("Period_in", {}).get("value")
                period_out = sensor_data.get("Period_out", {}).get("value")
            elif "Temperature" in sensor_name or "Temperature 2 (Ambience) Sensor" in sensor_name:
                temperature = sensor_data["Temperature"]["value"]
            elif "RH" in sensor_name or "Humidity" in sensor_name or "RH 2 (Ambience) Sensor" in sensor_name:
                humidity = sensor_data["RH"]["value"]
            elif "Illumination" in sensor_name:
                illumination = sensor_data.get("value")
            #people counter AI
            elif "Battery Node Sensor" in sensor_name:
                battery_node = sensor_data["Battery_Node"]["value"]
            #Ambience Sensor
            elif "CO2 Sensor" in sensor_name:
                co2 = sensor_data["CO2"]["value"]
            elif "HCHO Sensor" in sensor_name:
                hcho = sensor_data["HCHO"]["value"]
            elif "Light Level Sensor" in sensor_name:
                light_level = sensor_data["Light_Level"]["value"]
            elif "Passive Infra-Red Sensor" in sensor_name:
                pir_trigger = sensor_data["PIR"]["value"]
            elif "PM10 Sensor" in sensor_name:
                pm10 = sensor_data["PM10"]["value"]
            elif "PM2.5 Sensor" in sensor_name:
                pm2_5 = sensor_data["PM2_5"]["value"]
            elif "Pressure Sensor" in sensor_name:
                pressure = sensor_data["Pressure"]["value"]
            elif "TVOC Sensor" in sensor_name:
                tvoc = sensor_data["TVOC"]["value"]

    raw_data = sensor_readings  # Keep as dict/list

    try:
        if table_name == "People_Counter":
            cursor.execute("""
                INSERT INTO People_Counter (
                timestamp, device_type, device_name, location, sublocation, 
                battery_main, battery_node, total_in, total_out, period_in, period_out, raw_data
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            timestamp, device_type, device_name, location, sublocation,
            battery_main, battery_node, total_in, total_out, period_in, period_out, Json(raw_data)
        ))

        elif table_name == "AI_People_Counter":
            cursor.execute("""
                INSERT INTO AI_People_Counter (
                    timestamp, device_type, device_name, location, sublocation, 
                    region_counts_1, region_counts_2, region_counts_3, region_counts_4, 
                    region_counts_5, region_counts_6, region_counts_7, region_counts_8, raw_data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                timestamp, device_type, device_name, location, sublocation,
                region_counts_1, region_counts_2, region_counts_3, region_counts_4,
                region_counts_5, region_counts_6, region_counts_7, region_counts_8, json.dumps(sensor_readings)
            ))

        elif table_name == "Sound_Level_Monitoring":
            cursor.execute("""
                           INSERT INTO Sound_Level_Monitoring (timestamp, device_type, device_name, location,
                                                               sublocation,
                                                               battery_voltage, la_max, la_eq, la, raw_data)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           """, (
                               timestamp, device_type, device_name, location, sublocation,
                               battery_voltage, la_max, la_eq, la, Json(sensor_readings)
                           ))


        elif table_name == "Environmental_Monitoring":
            cursor.execute("""
                INSERT INTO Environmental_Monitoring (timestamp, device_type, device_name, location, sublocation, temperature, humidity, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (timestamp, device_type, device_name, location, sublocation, temperature, humidity, Json(raw_data)))

        # elif table_name == "ToF_People_Counter":
        #     cursor.execute("""
        #         INSERT INTO ToF_People_Counter (timestamp, device_type, device_name, location, sublocation, total_in,total_out, raw_data)
        #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        #     """, (timestamp, device_type, device_name, location, sublocation, total_in, total_out, Json(raw_data)))

        elif table_name == "Multi_Sensor_Monitoring":
            cursor.execute("""
                INSERT INTO Multi_Sensor_Monitoring (timestamp, device_type, device_name, location, sublocation, illumination, temperature, humidity, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (timestamp, device_type, device_name, location, sublocation, illumination, temperature, humidity, Json(raw_data)))

        elif table_name == "Ambience_Monitoring":
            cursor.execute("""
                           INSERT INTO Ambience_Monitoring (timestamp, device_type, device_name, location, sublocation,
                                                            co2, hcho, light_level, pir_trigger, pm10, pm2_5, pressure,
                                                            humidity, temperature, tvoc, raw_data)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           """, (
                               timestamp, device_type, device_name, location, sublocation,
                               co2, hcho, light_level, pir_trigger, pm10, pm2_5, pressure, humidity, temperature, tvoc,
                               Json(sensor_readings)
                           ))

        else:
            cursor.execute("""
                INSERT INTO Unknown_Devices (timestamp, device_type, device_name, location, sublocation, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (timestamp, device_type, device_name, location, sublocation, Json(raw_data)))

        conn.commit()
        print(f"Stored in PostgreSQL Table: {table_name}")

    except psycopg2.Error as e:
        conn.rollback()
        logging.error(f"Error inserting data into PostgreSQL: {e}")

def consume_messages():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None or msg.value() is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue

            try:
                sensor_data = json.loads(msg.value().decode('utf-8'))
                store_data(sensor_data)
            except json.JSONDecodeError as e:
                logging.error(f"JSON decoding error: {e}")

    except KeyboardInterrupt:
        print("\nShutting down consumer gracefully...")
    finally:
        consumer.close()
        cursor.close()
        conn.close()

# Start consumer loop
consume_messages()
