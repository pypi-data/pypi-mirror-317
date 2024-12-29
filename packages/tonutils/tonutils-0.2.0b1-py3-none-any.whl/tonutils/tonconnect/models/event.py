from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Union


class Event(str, Enum):
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    TRANSACTION = "transaction"


class EventError(str, Enum):
    CONNECT = "connect_error"
    DISCONNECT = "disconnect_error"
    TRANSACTION = "transaction_error"


EventHandler = Callable[..., Awaitable[None]]
EventHandlers = Dict[Union[Event, EventError], List[EventHandler]]
EventHandlersData = Dict[Union[Event, EventError], Dict[str, Any]]
