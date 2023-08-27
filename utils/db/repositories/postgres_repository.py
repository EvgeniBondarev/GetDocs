from .base_repository import BaseRepository
from sqlalchemy import select

from utils.db.schemas.record import Record

class PostgresRepository(BaseRepository):

    def __init__(self, connection_string):
        super().__init__(connection_string)

    async def full_text_search(self, keyword: str, max_records: int = 30) -> list[Record]:
        async with self.async_session() as session:
            stmt = select(Record).where(Record.description.match(keyword)).limit(max_records)
            result = await session.execute(stmt)

            records = result.scalars().all()
            return records