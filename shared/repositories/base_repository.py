# repositories/base_repository.py
import pymysql
from typing import List, Dict, Any
import config

class BaseRepository:
    def __init__(self, table_name: str):
        self.table = table_name
        self.db = pymysql.connect(
            host=config.MYSQL_HOST,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def get_all(self) -> List[Dict]:
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table}")
            return cursor.fetchall()

    def get_by_id(self, id_value: Any) -> Dict:
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id_value,))
            return cursor.fetchone()

    def create(self, data: Dict):
        keys = ", ".join(data.keys())
        values = tuple(data.values())
        placeholders = ", ".join(["%s"] * len(data))
        with self.db.cursor() as cursor:
            cursor.execute(f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})", values)
            return cursor.lastrowid

    def update(self, id_value: Any, data: Dict):
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
        values = tuple(data.values()) + (id_value,)
        with self.db.cursor() as cursor:
            cursor.execute(f"UPDATE {self.table} SET {set_clause} WHERE id=%s", values)

    def delete(self, id_value: Any):
        with self.db.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.table} WHERE id=%s", (id_value,))
