from flask import Flask
from flask_socketio import SocketIO

from routes.sensor_routes import sensor_bp
from services.websocket_service import set_socketio_instance

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

def create_app():
    app.register_blueprint(sensor_bp)
    set_socketio_instance(socketio)
    return app, socketio
