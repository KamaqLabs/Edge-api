from flask import Blueprint, jsonify
from sensors.repositories.sensor_repository import SensorRepository


sensor_bp = Blueprint("sensor_bp", __name__)
repo = SensorRepository()

@sensor_bp.route("/devices/<device_id>/sensors", methods=["GET"])
def get_sensors(device_id):
    sensors = repo.get_by_device(device_id)
    return jsonify(sensors)
