from abc import ABC, abstractmethod

from utils.db.schemas.record import Record


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

