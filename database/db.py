import mysql.connector
from config.settings import settings

def get_db_connection():
    return mysql.connector.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASS,
        database=settings.MYSQL_DB,
        port=settings.MYSQL_PORT
    )

def ensure_sensors_table() -> None:
    print("✔ Ensuring sensors table exists...")
    sql = """
    CREATE TABLE IF NOT EXISTS sensors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        device VARCHAR(100),
        sensor VARCHAR(250),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_device_sensor (device, sensor)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("✔ sensors table ensured")
    except Exception as e:
        print("❌ Error ensuring sensors table:", e)