from .base_repository import BaseRepository
import aiosqlite

from utils.db.schemas.record import Record

class SqliteRepository(BaseRepository):

    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.db_file_path = str(self.connection_string).replace("sqlite+aiosqlite:///", '')

    async def full_text_search(self, user_filter: str, max_records: id = 50) -> list[Record]:
        await self.__init_virtual_table()
        async with aiosqlite.connect(self.db_file_path) as db:
            async with db.execute('''SELECT id FROM labs_data_fts WHERE description MATCH ? ORDER BY rank''', (user_filter,)) as cursor:
                records_id = await cursor.fetchall()

            if not records_id:
                return None

            if len(records_id) > max_records:
                records = records_id[:max_records]
            else:
                records = records_id

            print(records)
            return [await self.get_record_by_id(record[0]) for record in records]

    async def __init_virtual_table(self):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS labs_data_fts USING FTS5(id, description, tokenize='porter')""")
            await db.commit()

            async with db.execute("""SELECT * FROM labs_data_fts""") as cursor:
                virtual_data = await cursor.fetchall()
                if virtual_data == []:
                    await self.__fill_virtual_table()

    async def __fill_virtual_table(self):
        async with aiosqlite.connect(self.db_file_path) as db:
            await db.execute("""INSERT INTO labs_data_fts(id, description) SELECT id, description FROM labs_data""")
            await db.commit()