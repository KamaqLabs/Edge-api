import paho.mqtt.client as mqtt
from db import get_connection

BROKER = "localhost"   # o test.mosquitto.org
TOPIC = "esp32/sensor"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Mensaje recibido en {msg.topic}: {payload}")

    # Guardar en MySQL
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO sensor_data (topic, value) VALUES (%s, %s)", (msg.topic, payload))
    db.commit()
    cursor.close()
    db.close()

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_start()
    return client
