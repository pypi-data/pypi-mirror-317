from abc import ABC, abstractmethod
from typing import Optional


class IStorage(ABC):
    KEY_LAST_EVENT_ID = "last_event_id"
    KEY_CONNECTION = "connection"
    ID = 0

    def _get_key(self, key: str) -> str:
        return f"{self.ID}:{key}"

    @abstractmethod
    async def set_item(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    async def get_item(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        pass

    @abstractmethod
    async def remove_item(self, key: str) -> None:
        pass
