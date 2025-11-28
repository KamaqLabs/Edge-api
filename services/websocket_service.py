import json

socketio = None

def set_socketio_instance(instance):
    """Recibe la instancia creada en app.py"""
    global socketio
    socketio = instance
    print("✔ SocketIO inicializado correctamente")


def emit_mqtt_message(topic, data):
    """Enviar datos a los clientes conectados via WebSocket"""
    if socketio is None:
        print("⚠ SocketIO aún no está inicializado — mensaje no enviado")
        return

    try:
        payload = json.loads(data)
        socketio.emit("new_data", {"topic": topic, "payload": payload})

        #print(f"📤 WS emit → {topic}: {data}")
    except Exception as e:
        print("❌ Error enviando por WebSocket:", e)