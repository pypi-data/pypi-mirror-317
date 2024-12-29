from __future__ import annotations

import asyncio
import inspect
import logging
import time
from typing import List, Tuple, Union

from pytoniq_core import Address, Cell, StateInit, begin_cell

from .exceptions import *
from .models import *
from .models.event import EventHandlers, EventHandlersData
from .provider.bridge import HTTPBridge
from .storage import IStorage
from ..utils import boc_to_base64_string, to_nano
from ..wallet.data import TransferData


class Connector:
    DISCONNECT_TIMEOUT = 600
    STANDARD_UNIVERSAL_URL = "tc://"

    class TransactionPendingContext:

        def __init__(self, connector: Connector, rpc_request_id: int):
            self.connector = connector
            self.rpc_request_id = rpc_request_id

        async def __aenter__(self) -> Union[TonConnectError, SendTransactionResponse]:
            return await self.connector._wait_for_pending_response(self.rpc_request_id)

        async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
            pass

    def __init__(
            self,
            user_id: int,
            manifest_url: str,
            storage: IStorage,
            api_tokens: Dict[str, str],
            on_events: EventHandlers,
            on_events_data: EventHandlersData,
    ) -> None:
        self.user_id = user_id
        self._manifest_url = manifest_url

        self._storage = storage
        self._bridge: Optional[HTTPBridge] = None
        self._wallet: Optional[WalletInfo] = None
        self._api_tokens = api_tokens

        self._on_events: EventHandlers = on_events
        self._events_data: EventHandlersData = on_events_data

        self._connect_timeout_task: Optional[asyncio.Task] = None

        self._pending_rpc_requests: Dict[int, Any] = {}
        self._condition_add_rpc_request: asyncio.Condition = asyncio.Condition()
        self._condition_receive_rpc_response: asyncio.Condition = asyncio.Condition()

    @property
    def is_connected(self) -> bool:
        return self._wallet is not None

    @property
    def wallet(self) -> Optional[WalletInfo]:
        return self._wallet if self.is_connected else None

    @property
    def account(self) -> Optional[Account]:
        return self._wallet.account if self.is_connected else None

    @property
    def device(self) -> Optional[DeviceInfo]:
        return self._wallet.device if self.is_connected else None

    @property
    def proof(self) -> Optional[TonProof]:
        return self._wallet.ton_proof if self.is_connected else None

    def add_event_kwargs(self, event: Event, **kwargs) -> None:
        self._events_data[event].update(kwargs)
        event_error = getattr(EventError, event.name)
        self._events_data[event_error].update(kwargs)

    async def _on_connect_wallet_timeout(self) -> None:
        await asyncio.sleep(HTTPBridge.DEFAULT_TTL)
        if self.is_connected:
            return

        await self._bridge.remove_session()
        payload = {"code": 500, "message": "Failed to connect: timeout."}
        response = {"event": EventError.CONNECT, "payload": payload}
        await self._on_wallet_status_changed(response)

    async def _on_wallet_status_changed(self, response: Dict[str, Any]) -> None:
        event = response.get("event")
        payload = response.get("payload")

        handlers = self._on_events.get(event, []).copy()
        kwargs = self._events_data.get(event, {}).copy()
        kwargs["user_id"] = self.user_id

        if event in {Event.CONNECT, Event.DISCONNECT}:
            kwargs["wallet"] = self._wallet
            if event == Event.CONNECT:
                self._wallet = WalletInfo.from_payload(payload)
                kwargs["wallet"] = self._wallet
            elif event == Event.DISCONNECT:
                self._wallet = None

        elif event in {EventError.CONNECT, EventError.DISCONNECT}:
            error = ConnectEventError.from_response(response)
            kwargs["error"] = error

        for handler in handlers:
            params = inspect.signature(handler).parameters
            await handler(**{k: v for k, v in kwargs.items() if k in params})

    async def _wait_for_added_request(self, rpc_request_id: int):
        async with self._condition_add_rpc_request:
            while rpc_request_id not in self._pending_rpc_requests:
                await self._condition_add_rpc_request.wait()

    async def _wait_for_pending_response(self, rpc_request_id: int) -> Union[TonConnectError, SendTransactionResponse]:
        async with self._condition_receive_rpc_response:
            while True:
                response = self._pending_rpc_requests.get(rpc_request_id)
                if response is not None:
                    self._pending_rpc_requests.pop(rpc_request_id)
                    return response
                await self._condition_receive_rpc_response.wait()

    async def __handle_transaction_response(self, response: Dict[str, Any], rpc_request_id: int) -> None:
        if not response:
            raise TonConnectError("Failed to send transaction: no response received.")

        error = SendTransactionEventError.from_response(response)
        event = EventError.TRANSACTION if error else Event.TRANSACTION

        handlers = self._on_events.get(event, []).copy()
        kwargs = self._events_data.get(event, {}).copy()
        kwargs.update({"user_id": self.user_id, "rpc_request_id": rpc_request_id})

        if error is not None:
            self._pending_rpc_requests[rpc_request_id] = error
            kwargs["error"] = error
        else:
            transaction = SendTransactionResponse.from_dict(response)
            self._pending_rpc_requests[rpc_request_id] = transaction
            kwargs["transaction"] = transaction

        for handler in handlers:
            params = inspect.signature(handler).parameters
            await handler(**{k: v for k, v in kwargs.items() if k in params})

        if bool(self._condition_receive_rpc_response._waiters):
            async with self._condition_receive_rpc_response:
                self._condition_receive_rpc_response.notify_all()
        else:
            self._pending_rpc_requests.pop(rpc_request_id)

    @staticmethod
    def __find_send_transaction_feature(
            features: List[Union[str, Dict[str, Any]]],
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        is_deprecated_supported = "SendTransaction" in features

        send_transaction_feature = None
        for feature in features:
            if isinstance(feature, dict) and feature.get("name") == "SendTransaction":
                send_transaction_feature = feature
                break

        return is_deprecated_supported, send_transaction_feature

    def __verify_send_transaction_feature(self, required_messages: int) -> None:
        features = self.wallet.device.features
        is_deprecated_supported, send_transaction_feature = self.__find_send_transaction_feature(features)

        if not is_deprecated_supported and not send_transaction_feature:
            raise WalletNotSupportFeatureError("Wallet does not support the SendTransaction feature.")

        if send_transaction_feature:
            max_messages = send_transaction_feature.get("maxMessages")

            if max_messages is not None:
                if max_messages < required_messages:
                    raise WalletNotSupportFeatureError(
                        f"Wallet cannot handle SendTransaction request: "
                        f"max supported messages {max_messages}, required {required_messages}."
                    )
            else:
                logging.warning(
                    "Connected wallet did not provide information about the maximum allowed messages "
                    "in the SendTransaction request. The request may be rejected by the wallet."
                )

    def __prepare_transaction(self, transaction: Transaction) -> None:
        required_messages = len(transaction.messages)
        self.__verify_send_transaction_feature(required_messages)

        timestamp = int(time.time())
        transaction.valid_until = transaction.valid_until or timestamp + 300
        transaction.from_ = transaction.from_ or self._wallet.account.address.to_str()
        transaction.network = transaction.network or self._wallet.account.chain
        transaction.messages = transaction.messages or []

    async def __process_transaction(
            self,
            transaction: Transaction,
            connection: Dict[str, Any],
            rpc_request_id: int,
    ) -> None:
        if not self.is_connected:
            raise TonConnectError("Wallet not connected.")

        async with self._condition_add_rpc_request:
            self._pending_rpc_requests[rpc_request_id] = None
            self._condition_add_rpc_request.notify_all()

        try:
            self.__prepare_transaction(transaction)
            request = SendTransactionRequest(params=[transaction])
            timeout = int(transaction.valid_until - int(time.time()))
            response = await asyncio.wait_for(
                self._bridge.send_request(request, connection, rpc_request_id),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            response = {"error": {"code": 500, "message": "Failed to send transaction: timeout."}}
        except Exception as e:
            response = {"error": {"code": 0, "message": f"Failed to send transaction: {e}"}}

        await self.__handle_transaction_response(response, rpc_request_id)

    async def _send_transaction(self, messages: List[Message]) -> int:
        transaction = Transaction(messages=messages)
        connection = await self._bridge.get_stored_connection_data()
        rpc_request_id = int(connection.get("next_rpc_request_id", "0"))

        loop = asyncio.get_running_loop()
        loop.create_task(self.__process_transaction(transaction, connection, rpc_request_id))
        await self._wait_for_added_request(rpc_request_id)

        return rpc_request_id

    async def connect_wallet(
            self,
            wallet_app: WalletApp,
            redirect_url: str = "back",
            ton_proof: Optional[str] = None,
    ) -> str:
        if self.is_connected:
            raise TonConnectError("Wallet is already connected.")
        if self._bridge:
            await self._bridge.close_connection()
        if self._connect_timeout_task and not self._connect_timeout_task.done():
            self._connect_timeout_task.cancel()

        self._bridge = HTTPBridge(
            storage=self._storage,
            bridge_url=wallet_app.bridge_url,
            on_status_changed=self._on_wallet_status_changed,
            api_tokens=self._api_tokens,
        )
        request = SendConnectRequest.create(self._manifest_url, ton_proof)
        universal_url = wallet_app.universal_url or self.STANDARD_UNIVERSAL_URL

        connect_universal_url = await self._bridge.connect(
            request=request,
            universal_url=universal_url,
            redirect_url=redirect_url,
        )

        loop = asyncio.get_running_loop()
        self._connect_timeout_task = loop.create_task(self._on_connect_wallet_timeout())
        return connect_universal_url

    async def restore_connection(self) -> None:
        if self._bridge:
            await self._bridge.close_connection()
        else:
            self._bridge = HTTPBridge(
                storage=self._storage,
                bridge_url="",
                on_status_changed=self._on_wallet_status_changed,
                api_tokens=self._api_tokens,
            )
        self._wallet = await self._bridge.restore_connection()

    async def disconnect_wallet(self) -> None:
        if not self.is_connected:
            raise WalletNotConnectedError

        try:
            connection = await self._bridge.get_stored_connection_data()
            rpc_request_id = int(connection.get("next_rpc_request_id", "0"))

            request = SendDisconnectRequest()
            await self._bridge.send_request_with_cleanup(
                request=request,
                connection=connection,
                rpc_request_id=rpc_request_id,
                timeout=self.DISCONNECT_TIMEOUT
            )
            response = {"event": Event.DISCONNECT}
        except asyncio.TimeoutError:
            response = {
                "event": EventError.DISCONNECT,
                "payload": {"code": 500, "message": "Failed to disconnect: timeout."}
            }
        except TonConnectError as e:
            response = {
                "event": EventError.DISCONNECT,
                "payload": {"code": 0, "message": f"Failed to disconnect: {e}"}
            }
        except Exception as e:
            response = {
                "event": EventError.DISCONNECT,
                "payload": {"code": 0, "message": f"An unexpected error occurred: {e}"}
            }
        finally:
            if self.is_connected:
                await self._bridge.remove_session()
        await self._on_wallet_status_changed(response)

    async def is_transaction_pending(self, rpc_request_id: int) -> bool:
        async with self._condition_add_rpc_request:
            return rpc_request_id in self._pending_rpc_requests

    def pending_transaction_context(self, rpc_request_id: int) -> Connector.TransactionPendingContext:
        if rpc_request_id not in self._pending_rpc_requests:
            raise TonConnectError(f"Request {rpc_request_id} is not pending.")
        return Connector.TransactionPendingContext(self, rpc_request_id)

    def get_max_supported_messages(self) -> Optional[int]:
        _, feature = self.__find_send_transaction_feature(self.wallet.device.features)
        return feature.get("maxMessages") if feature else None

    @staticmethod
    def create_transfer_message(
            destination: Union[Address, str],
            amount: Union[float, int],
            body: Optional[Cell] = None,
            state_init: Optional[StateInit] = None,
            **_,
    ) -> Message:
        if isinstance(destination, Address):
            destination = destination.to_str()
        if isinstance(body, str):
            body = (
                begin_cell()
                .store_uint(0, 32)
                .store_snake_string(body)
                .end_cell()
            )
        if body is not None:
            body = boc_to_base64_string(body.to_boc())
        if state_init is not None:
            state_init = boc_to_base64_string(state_init.serialize().to_boc())

        return Message(
            address=destination,
            amount=str(to_nano(amount)),
            payload=body,
            state_init=state_init,
        )

    async def send_transfer(
            self,
            destination: Union[Address, str],
            amount: Union[float, int],
            body: Optional[Union[Cell, str]] = None,
            state_init: Optional[StateInit] = None,
    ) -> int:
        message = self.create_transfer_message(destination, amount, body, state_init)
        return await self._send_transaction([message])

    async def send_batch_transfer(self, data_list: List[TransferData]) -> int:
        messages = [self.create_transfer_message(**transfer_data.__dict__) for transfer_data in data_list]
        return await self._send_transaction(messages)

    async def pause(self) -> None:
        if self._bridge:
            await self._bridge.pause_sse()

    async def unpause(self) -> None:
        if self._bridge:
            await self._bridge.start_sse()
