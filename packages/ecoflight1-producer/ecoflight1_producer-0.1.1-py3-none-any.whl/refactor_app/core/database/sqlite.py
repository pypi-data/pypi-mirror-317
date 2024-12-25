"""
Модуль для инициализации Sqlite базы

"""

import sqlite3


def create_database() -> None:
    """Функция инициализации базы данных"""

    NAMES_DB = "database.db"

    TABLES_NAME = ["noise", "notifications", "events", "noise_records", "raw_noise_audio"]

    SQLITE_COLUMNS = {
        "noise": (
            "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL",
            "la_max REAL NOT NULL",
            "la_eq REAL NOT NULL",
            "la_eq_hour REAL NOT NULL",
            "rta TEXT NOT NULL",
            "dt REAL NOT NULL",
            "time_stamp CHAR(50) NOT NULL",
            "sensor_name CHAR(30) NOT NULL",
            "message_type CHAR(30) NOT NULL",
        ),
        "notifications": (
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "notification_id CHAR(50) NOT NULL",
            "sensor_name CHAR(30) NOT NULL",
            "message_type CHAR(30)",
            "threshold INT",
            "notification_ts DATETICHAR(50)",
            "notification_type CHAR(10)",
        ),
        "events": (
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "event_id CHAR(50) NOT NULL",
            "sensor_name CHAR(30) NOT NULL",
            "message_type CHAR(30)",
            "event_type CHAR(10)",
            "threshold INT",
            "time_stamp_start CHAR(50)",
            "event_la_max REAL",
            "time_stamp_max CHAR(50)",
            "time_stamp_end CHAR(50)",
        ),
        "noise_records": (
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "event_id INTEGER NOT NULL",
            "bucket_name TEXT NOT NULL",
            "object_name TEXT NOT NULL",
            "duration REAL",
            "file_size_bytes INTEGER",
            "message_type TEXT",
            "sent_status TEXT",
        ),
        "raw_noise_audio": (
            "id INTEGER PRIMARY KEY AUTOINCREMENT",
            "event_id INTEGER NOT NULL",
            "data blob NOT NULL",
            "time_stamp_start CHAR(50)",
        )
    }

    with sqlite3.connect(database=NAMES_DB) as conn:
        cursor = conn.cursor()

        for table in TABLES_NAME:
            column_definitions = ", ".join(SQLITE_COLUMNS[table])
            create_table_query = f" CREATE TABLE IF NOT EXISTS {table} ({column_definitions})"
            cursor.execute(create_table_query)


def get_connection_sqlite() -> sqlite3.Connection:
    return sqlite3.connect(database="database.db")
