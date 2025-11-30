from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MQTT_HOST = os.getenv("MQTT_HOST")
    MQTT_PORT = int(os.getenv("MQTT_PORT"))
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASS = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")
    MQTT_USERNAME = os.getenv("MQTT_USERNAME")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
    MQTT_TLS = os.getenv("MQTT_TLS", "false").lower() == "true"

    FLASK_PORT = int(os.getenv("FLASK_PORT"))

settings = Settings()
