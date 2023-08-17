from repository import DatabaseType, AbstractRepository, SqliteRepository, PostgresRepository


class DatabaseManager:

    def __init__(self, db_type: DatabaseType, connection_string: str):
        self.db_type = db_type
        self.connection_string = connection_string

    def get_repository(self) -> AbstractRepository:
        if self.db_type == DatabaseType.SQLITE:
            return SqliteRepository(self.connection_string)
        elif self.db_type == DatabaseType.POSTGRES:
            return PostgresRepository(self.connection_string)
        else:
            raise ValueError("Unsupported database type")


# db_manager = DatabaseManager(db_type=DatabaseType.SQLITE, connection_string="sqlite://database.db")
# repository = db_manager.get_repository()
#
# record = repository.get_record_by_id(1)гмшсщ