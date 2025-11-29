import eventlet
eventlet.monkey_patch()

from app import create_app
from database.db import ensure_sensors_table
from mqtt.client import create_mqtt_client

if __name__ == "__main__":
    # Crear tabla si no existe
    ensure_sensors_table()

    # Inicializar Flask + SocketIO
    app, socketio = create_app()

    # Inicializar MQTT y loop
    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    # Iniciar servidor con WebSockets
    socketio.run(app, host="0.0.0.0", port=5000)
