import ssl

import paho.mqtt.client as mqtt


from config.settings import settings
from database.db import get_db_connection
from services.sensor_service import process_sensor_message
import json

from services.websocket_service import emit_mqtt_message


def _device_has_sensors(device: str) -> bool:
    """Return True if there are sensors already registered for `device` in DB."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sensors WHERE device = %s", (device,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    except Exception as e:
        print("Error comprobando sensores en DB:", e)
        # Si hay error, mejor no bloquear el procesamiento; asumir que no existen
        return False



def on_connect(client, userdata, flags, rc):
    print("MQTT conectado:", rc)
    client.subscribe("esp32/#")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"📥 MQTT | {topic} → {payload}")

    # Si es el topic especial → Guardar sensores
    if topic == "esp32/info/sensors":
        try:
            data = json.loads(payload)
            device = data["device"]
            sensors = data["sensors"]
            if _device_has_sensors(device):
                print(f"🔕 Sensores ya registrados para device '{device}' — no se guardará nada.")
                return
            for s in sensors:
                process_sensor_message(device, s)

            print("Sensores registrados correctamente en DB.")
        except Exception as e:
            print("Error procesando sensores:", e)

        return  # NO enviamos a socket en este caso

    # -----------------------------
    # Para cualquier otro topic → Enviar al frontend por SocketIO
    # -----------------------------
    try:
        emit_mqtt_message(topic, payload)
    except Exception as e:
        print("❌ Error enviando por socket:", e)



def create_mqtt_client():
    client = mqtt.Client()

    # Si tienes usuario/contraseña en el broker
    if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    # Si el puerto es 8883 -> usar TLS
    if str(settings.MQTT_PORT) == "8883" or settings.MQTT_TLS is True:
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.tls_insecure_set(True)
        print("🔐 Usando conexión MQTT con TLS")

    print(f"🔌 Conectando a MQTT → {settings.MQTT_HOST}:{settings.MQTT_PORT}...")
    client.connect(settings.MQTT_HOST, int(settings.MQTT_PORT), 60)

    return client