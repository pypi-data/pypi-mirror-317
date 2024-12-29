from typing import Optional, Dict

from .base import IStorage


class MemoryStorage(IStorage):
    DATA: Dict[str, str] = {}

    async def set_item(self, key: str, value: str) -> None:
        key = self._get_key(key)
        self.DATA[key] = value

    async def get_item(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        key = self._get_key(key)
        if key not in self.DATA:
            return default_value
        return self.DATA.get(key)

    async def remove_item(self, key: str) -> None:
        key = self._get_key(key)
        if key in self.DATA:
            del self.DATA[key]
