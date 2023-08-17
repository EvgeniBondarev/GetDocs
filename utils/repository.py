from abc import ABC, abstractmethod
import sqlite3
from sqlite3 import Error
from enum import Enum

from models.record import Record, render_record_model


class DatabaseType(Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
class AbstractRepository(ABC):
    @abstractmethod
    def get_record_by_id(self, record_id: int) -> Record:
        raise NotImplementedError

    @abstractmethod
    def get_records_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_records_in_range(self, page_number: int, range: int) -> list[Record]:
        raise NotImplementedError

    @abstractmethod
    def set_record_visibility(self, record_id: int):
        raise NotImplementedError

    @abstractmethod
    def full_text_search(self, user_filter: str):
        raise NotImplementedError

class SqliteRepository(AbstractRepository):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_record_by_id(self, record_id: int) -> Record:
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.execute("SELECT * FROM labs_data WHERE id=?", (record_id,))
            base_record = cursor.fetchone()
            return render_record_model(base_record)

    def get_records_count(self) -> int:
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM labs_data")
            records_count = cursor.fetchone()
            return records_count[0]

    def get_records_in_range(self, page_number: int, range: int = 20) -> list[Record]:
        lower_bound = (page_number - 1) * range + 1
        upper_bound = page_number * range

        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.execute("SELECT * FROM labs_data WHERE id BETWEEN ? AND ?", (lower_bound, upper_bound))
            base_records_in_range = cursor.fetchall()
            records_in_range = [render_record_model(record) for record in base_records_in_range]

            return records_in_range

    def set_record_visibility(self, record_id: int):
        raise NotImplementedError

    def full_text_search(self, user_filter: str, max_records: int = 50) -> list[Record]:
        self.__init_virtual_table()
        with sqlite3.connect(self.connection_string) as conn:
            cursor = conn.execute("SELECT id FROM labs_data_fts WHERE description MATCH ? ORDER BY rank", (user_filter,))
            records_id = cursor.fetchall()

        if not records_id:
            return None

        if len(records_id) > max_records:
            records = records_id[:max_records]
        else:
            records = records_id

        return [self.get_record_by_id(record[0]) for record in records]

    def __init_virtual_table(self):
        with sqlite3.connect(self.connection_string) as conn:
            conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS labs_data_fts USING FTS5(id, description, tokenize='porter')")
            conn.commit()

            cursor = conn.execute("SELECT * FROM labs_data_fts")
            virtual_data = cursor.fetchall()
            if not virtual_data:
                self.__fill_virtual_table()

    def __fill_virtual_table(self):
        with sqlite3.connect(self.connection_string) as conn:
            conn.execute("INSERT INTO labs_data_fts(id, description) SELECT id, description FROM labs_data")
            conn.commit()


class PostgresRepository(AbstractRepository):

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_record_by_id(self, record_id: int) -> Record:
        raise NotImplementedError

    def get_records_count(self) -> int:
        raise NotImplementedError

    def get_records_in_range(self, page_number: int, range: int) -> list[Record]:
        raise NotImplementedError

    def set_record_visibility(self, record_id: int):
        raise NotImplementedError

    def full_text_search(self, user_filter: str):
        raise NotImplementedError