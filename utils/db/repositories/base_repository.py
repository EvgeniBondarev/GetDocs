from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from .abstract_repository import AbstractRepository
from utils.db.schemas.record import Record


class BaseRepository(AbstractRepository):
     def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_async_engine(connection_string, echo=True)
        self.async_session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

     async def get_record_by_id(self, record_id: int) -> Record:
        async with self.async_session() as session:
            try:
                record = await session.execute(select(Record).where(Record.id == record_id))
                return record.scalar_one()
            except Exception:
                return None

     async def get_records_count(self) -> int:
            async with self.async_session() as session:
                query = select(func.count()).select_from(Record)
                records_count = await session.execute(query)
                total_records = records_count.scalar()

                return total_records

     async def get_records_in_range(self, page_number: int, range: int = 20) -> list[Record]:
        lower_bound = (page_number - 1) * range + 1
        upper_bound = page_number * range

        async with self.engine.begin() as conn:
            query = select(Record).where(Record.id.between(lower_bound, upper_bound))
            result = await conn.execute(query)
            records_in_range = result.all()

        return records_in_range

     def set_record_visibility(self, record_id: int):
        raise NotImplementedError



