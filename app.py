from flask import Flask
from flask_socketio import SocketIO
import json
import ssl
import paho.mqtt.client as mqtt
import config
from sensors.routes.sensor_routes import sensor_bp
from shared.create_table import create_tables
import pymysql

from sensors.repositories.sensor_repository import SensorRepository

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
app.register_blueprint(sensor_bp, url_prefix="/api/v1")

sensor_repo = SensorRepository()


# --- Conexión MySQL ---
db = pymysql.connect(host=config.MYSQL_HOST, user=config.MYSQL_USER, password=config.MYSQL_PASSWORD, database=config.MYSQL_DB, autocommit=False)

# call when you want to ensure tables exist (e.g., at startup)
create_tables(db)

# --- MQTT callbacks ---
def on_connect(client, userdata, flags, rc):
    """Callback for API v1 (4 parameters)"""
    print("Conectado a MQTT con código", rc)
    topics = [
        "esp32/data/smoke",
        "esp32/data/temperature",
        "esp32/data/motion"
    ]
    for t in topics:
        client.subscribe(t)
        print("Suscrito a", t)

def on_connect_v2(client, userdata, flags, rc, properties):
    """Callback for API v2 (5 parameters)"""
    print("Conectado con código:", rc)
    topics = [
        "esp32/data/smoke",
        "esp32/data/temperature",
        "esp32/data/motion",
        "esp32/info/sensors"
    ]
    for t in topics:
        client.subscribe(t)
        print("Suscrito a", t)


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        data = json.loads(msg.payload.decode())

        if topic == "esp32/data/smoke":
            print("🔥 Datos de humo:", data)
        elif topic == "esp32/data/temperature":
            print("🌡️ Datos de temperatura:", data)
        elif topic == "esp32/data/motion":
            print("🚶 Datos de movimiento:", data)
        elif topic == "esp32/info/sensors":
            device = data.get("device")
            sensors = data.get("sensors", [])
            if device and sensors:
                sensor_repo.delete_by_device(device)
                for name in sensors:
                    sensor_repo.create({"device_id": device, "name": name})
                print(f"✅ Actualizada lista de sensores para {device}")

        socketio.emit("new_data", {"topic": topic, "payload": data})

    except Exception as e:
        print(f"⚠️ Error procesando mensaje MQTT: {e}")


# --- MQTT Client ---
use_v2 = False
try:
    mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    use_v2 = True
    print("Using paho-mqtt callback API v2")
except (TypeError, RuntimeError, AttributeError):
    mqtt_client = mqtt.Client()
    print("callback_api_version=2 not supported, falling back to default client")

mqtt_client.username_pw_set(config.MQTT_USER, config.MQTT_PASS)

# Use tls_set_context if available, otherwise try a safer fallback
if hasattr(mqtt_client, "tls_set_context"):
    mqtt_client.tls_set_context(ssl.create_default_context())
elif hasattr(mqtt_client, "tls_set"):
    try:
        mqtt_client.tls_set()
    except Exception:
        pass

# Assign the correct callback based on API version
mqtt_client.on_connect = on_connect_v2 if use_v2 else on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
mqtt_client.loop_start()



if __name__ == "__main__":
    # For development only: allow Werkzeug (use a production WSGI server for production)
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
