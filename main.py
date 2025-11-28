from app import create_app
from database.db import ensure_sensors_table
from mqtt.client import create_mqtt_client
from config.settings import settings

if __name__ == "__main__":
    ensure_sensors_table()
    app, socketio = create_app()

    mqtt_client = create_mqtt_client()
    mqtt_client.loop_start()

    socketio.run(app, host="0.0.0.0", port=settings.FLASK_PORT, allow_unsafe_werkzeug=True)