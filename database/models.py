from database.db import get_db_connection

def save_sensor_definition(device, sensor):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO sensors (device, sensor)
    VALUES (%s, %s)
    """

    cursor.execute(query, (device, sensor))
    conn.commit()

    cursor.close()
    conn.close()


def get_all_sensors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sensors")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows