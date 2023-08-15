from abc import ABC, abstractmethod
import aiosqlite

from models.record import Record, render_record_model

class AbstractRepository(ABC):

    @abstractmethod
    async def get_record_by_id(self, record_id: int) -> Record:
        raise NotImplementedError

    @abstractmethod
    async def get_records_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_records_in_range(self, page_number: int, range: int) -> list[Record]:
        raise NotImplementedError

    @abstractmethod
    async def set_record_visibility(self, record_id: int):
        raise NotImplementedError

    @abstractmethod
    async def full_text_search(self, user_filter: str):
        raise NotImplementedError

class AioSqliteRepository(AbstractRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def get_record_by_id(self, record_id: int) -> Record:
        async with aiosqlite.connect(self.connection_string) as db:
            async with db.execute("""SELECT * FROM labs_data WHERE id=%d""" % record_id) as cursor:
                base_record = await cursor.fetchone()
                return await render_record_model(base_record)

    async def get_records_count(self) -> int:
        async with aiosqlite.connect(self.connection_string) as db:
            async with db.execute("""SELECT COUNT(*) FROM labs_data""") as cursor:
                records_count = await cursor.fetchone()
                return records_count[0]


    async def get_records_in_range(self, page_number: int, range: int = 20) -> list[Record]:
        lower_bound = (page_number - 1) * range + 1
        upper_bound = page_number * range

        async with aiosqlite.connect(self.connection_string) as db:
            async with db.execute("""SELECT * FROM labs_data WHERE id BETWEEN %d AND %d""" % (lower_bound, upper_bound)) as cursor:
                base_records_in_range = await cursor.fetchall()
                records_in_range = [await render_record_model(record) for record in base_records_in_range]

                return records_in_range

    async def set_record_visibility(self, record_id: int):
        raise NotImplementedError

    async def full_text_search(self, user_filter: str, max_records: id = 50) -> list[Record]:
        await self.__init_virtual_table()
        async with aiosqlite.connect(self.connection_string) as db:
            async with db.execute('''SELECT id FROM labs_data_fts WHERE description MATCH ? ORDER BY rank''', (user_filter,)) as cursor:
                records_id = await cursor.fetchall()

            if not records_id:
                return None

            if len(records_id) > max_records:
                records = records_id[:max_records]
            else:
                records = records_id

            return [await self.get_record_by_id(record) for record in records]

    async def __init_virtual_table(self):
        async with aiosqlite.connect(self.connection_string) as db:
            await db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS labs_data_fts USING FTS5(id, description, tokenize='porter')""")
            await db.commit()

            async with db.execute("""SELECT * FROM labs_data_fts""") as cursor:
                virtual_data = await cursor.fetchall()
                if virtual_data == []:
                    await self.__fill_virtual_table()

    async def __fill_virtual_table(self):
        async with aiosqlite.connect(self.connection_string) as db:
            await db.execute("""INSERT INTO labs_data_fts(id, description) SELECT id, description FROM labs_data""")
            await db.commit()

