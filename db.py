from dataclasses import dataclass
import os

import mysql.connector


@dataclass
class DatabaseConfig:
    host: str
    user: str
    password: str
    database: str
    port: int = 3306



def _load_config(prefix: str) -> DatabaseConfig:
    return DatabaseConfig(
        host=os.environ.get(f"{prefix}_DB_HOST", "localhost"),
        user=os.environ.get(f"{prefix}_DB_USER", "root"),
        password=os.environ.get(f"{prefix}_DB_PASSWORD", ""),
        database=os.environ.get(f"{prefix}_DB_NAME", ""),
        port=int(os.environ.get(f"{prefix}_DB_PORT", "3306")),
    )


def get_registration_connection():
    config = _load_config("REGISTRATION")
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database,
        port=config.port,
    )


def get_attendance_connection():
    config = _load_config("ATTENDANCE")
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database,
        port=config.port,
    )
