from flask import Blueprint, jsonify

from services.sensor_service import get_sensors

sensor_bp = Blueprint("sensor", __name__)

@sensor_bp.route("/api/v1/sensors", methods=["GET"])
def get_all_sensors():
    data = get_sensors()
    return jsonify(data)

@sensor_bp.route("/api/v1/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})