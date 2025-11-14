
def create_tables(db, commit=True):
    """Create required tables if they don't exist. Commits by default."""
    create_sensors_sql = """
    CREATE TABLE IF NOT EXISTS sensors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(100) NOT NULL,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY ux_device_name (device_id, name)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    create_sensor_data_sql = """
    CREATE TABLE IF NOT EXISTS sensor_data (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        device_id VARCHAR(100) NOT NULL,
        sensor_name VARCHAR(100) NOT NULL,
        value DOUBLE,
        payload JSON,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_device_time (device_id, timestamp)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    try:
        with db.cursor() as cursor:
            cursor.execute(create_sensors_sql)
            cursor.execute(create_sensor_data_sql)
        if commit:
            db.commit()
    except Exception:
        try:
            db.rollback()
        except Exception:
            pass
        raise
