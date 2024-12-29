import asyncio
from copy import copy
from typing import Optional, List, Dict, Callable

from .connector import Connector
from .exceptions import TonConnectError
from .models import WalletApp
from .models.event import (
    Event,
    EventError,
    EventHandler,
    EventHandlers, EventHandlersData,
)
from .storage import IStorage
from .wallet_manager import WalletsListManager


class TonConnect:
    def __init__(
            self,
            storage: IStorage,
            manifest_url: str,
            api_tokens: Optional[Dict[str, str]] = None,
            exclude_wallets: Optional[List[str]] = None,
            include_wallets: Optional[List[str]] = None,
            wallets_list_cache_ttl: Optional[int] = None,
            wallets_list_source_url: Optional[str] = None,
    ) -> None:
        self.storage = storage
        self.manifest_url = manifest_url
        self.api_tokens = api_tokens

        self._wallets_list_manager = WalletsListManager(
            source_url=wallets_list_source_url,
            include_wallets=include_wallets,
            exclude_wallets=exclude_wallets,
            cache_ttl=wallets_list_cache_ttl,
        )

        self._event_handlers = self.__initialize_event_handlers()
        self._events_data = self.__initialize_events_data()

        self._connectors: Dict[int, Connector] = {}
        self._connectors_lock = asyncio.Lock()

    @staticmethod
    def __initialize_event_handlers() -> EventHandlers:
        return {
            Event.CONNECT: [],
            EventError.CONNECT: [],
            Event.DISCONNECT: [],
            EventError.DISCONNECT: [],
            Event.TRANSACTION: [],
            EventError.TRANSACTION: [],
        }

    @staticmethod
    def __initialize_events_data() -> EventHandlersData:
        return {
            Event.CONNECT: {},
            EventError.CONNECT: {},
            Event.DISCONNECT: {},
            EventError.DISCONNECT: {},
            Event.TRANSACTION: {},
            EventError.TRANSACTION: {},
        }

    def __init_user_storage(self, user_id: int) -> IStorage:
        user_storage = copy(self.storage)
        user_storage.ID = user_id
        return user_storage

    async def get_wallets(self) -> List[WalletApp]:
        return await self._wallets_list_manager.get_wallets()

    def on_event(self, event: Event) -> Callable[[EventHandler], EventHandler]:
        def decorator(handler: EventHandler) -> EventHandler:
            if event not in self._event_handlers:
                self._event_handlers[event] = []
            self._event_handlers[event].append(handler)
            return handler

        return decorator

    def on_event_error(self, event: EventError) -> Callable[[EventHandler], EventHandler]:
        def decorator(handler: EventHandler) -> EventHandler:
            if event not in self._event_handlers:
                self._event_handlers[event] = []
            self._event_handlers[event].append(handler)
            return handler

        return decorator

    async def create_connector(self, user_id: int) -> Connector:
        user_storage = self.__init_user_storage(user_id)
        connector = Connector(
            user_id=user_id,
            manifest_url=self.manifest_url,
            storage=user_storage,
            on_events=self._event_handlers,
            on_events_data=self._events_data,
            api_tokens=self.api_tokens or {},
        )
        self._connectors[user_id] = connector

        return connector

    async def init_connector(self, user_id: int) -> Connector:
        async with self._connectors_lock:
            if user_id in self._connectors:
                connector = self._connectors[user_id]
            else:
                connector = await self.create_connector(user_id)
            try:
                await connector.restore_connection()
            except TonConnectError:
                pass
            return connector

    async def run_all(self, user_ids: List[int]) -> None:
        async with self._connectors_lock:
            for user_id in user_ids:
                await self.create_connector(user_id)

    async def close_all(self) -> None:
        async with self._connectors_lock:
            pause_tasks = [connector.pause() for connector in self._connectors.values()]
        await asyncio.gather(*pause_tasks)
