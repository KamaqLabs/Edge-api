from flask import Flask
from flask_socketio import SocketIO

from database.db import ensure_sensors_table
from mqtt.client import create_mqtt_client
from routes.sensor_routes import sensor_bp
from services.websocket_service import set_socketio_instance

ensure_sensors_table()
mqtt_client = create_mqtt_client()
mqtt_client.loop_start()


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

def create_app():
    app.register_blueprint(sensor_bp)
    set_socketio_instance(socketio)
    return app, socketio




app, socketio = create_app()