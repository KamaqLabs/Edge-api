from database.models import save_sensor_definition, get_all_sensors


def process_sensor_message(device, s):
    save_sensor_definition(device, s)


def get_sensors():
    return get_all_sensors()