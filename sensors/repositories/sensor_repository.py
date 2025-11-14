
from shared.repositories.base_repository import BaseRepository

class SensorRepository(BaseRepository):
    def __init__(self):
        super().__init__("sensors")  # nombre de la tabla

    def get_by_device(self, device_id: str):
        with self.db.cursor() as cursor:
            cursor.execute("SELECT * FROM sensors WHERE device_id = %s", (device_id,))
            return cursor.fetchall()

    def delete_by_device(self, device_id: str):
        with self.db.cursor() as cursor:
            cursor.execute("DELETE FROM sensors WHERE device_id = %s", (device_id,))
