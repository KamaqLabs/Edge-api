from flask import Flask
from flask_socketio import SocketIO
from routes.sensor_routes import sensor_bp
from services.websocket_service import set_socketio_instance


def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

    app.register_blueprint(sensor_bp)

    # ✔ Después de registrar routes
    set_socketio_instance(socketio)

    return app, socketio
