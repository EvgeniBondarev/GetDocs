from .repositories.base_repository import AbstractRepository
from .database_type import DatabaseType, database_config
from .schemas.record import Record


class DatabaseClient(AbstractRepository):
    def __init__(self, db_type: DatabaseType):
        db_info = database_config.get(db_type)
        if db_info:
            connection_string = db_info["connection_string"]
            db_class = db_info["class"]

            self.repositoty: AbstractRepository = db_class(connection_string)
        else:
            raise ValueError("Unsupported database type")

    async def get_record_by_id(self, record_id: int) -> Record:
        return await self.repositoty.get_record_by_id(record_id)

    async def get_records_count(self) -> int:
        return await self.repositoty.get_records_count()


    async def get_records_in_range(self, page_number: int, range: int) -> list[Record]:
        return await self.repositoty.get_records_in_range(page_number, range)

    async def set_record_visibility(self, record_id: int) -> Record:
        return await self.repositoty.set_record_visibility(record_id)

    async def full_text_search(self, user_filter: str) -> list[Record]:
        return await self.repositoty.full_text_search(user_filter)