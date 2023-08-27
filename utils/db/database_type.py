from enum import Enum

from .repositories.postgres_repository import PostgresRepository
from .repositories.sqlite_repository import SqliteRepository
from config import SQLITE_URL, POSTGRES_URL

class DatabaseType(Enum):
    sqlite = "sqlite"
    postgresql = "postgresql"

database_config = {
    DatabaseType.sqlite: {
        "connection_string": SQLITE_URL,
        "class": SqliteRepository
    },
    DatabaseType.postgresql: {
        "connection_string": POSTGRES_URL,
        "class": PostgresRepository
    },
}
