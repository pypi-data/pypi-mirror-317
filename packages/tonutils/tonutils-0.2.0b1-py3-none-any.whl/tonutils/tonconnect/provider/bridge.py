import asyncio
import json
from typing import Awaitable, Callable, Dict, Optional, Any
from urllib.parse import urlencode, urlparse, parse_qs, quote_plus

import aiohttp

from ..exceptions import TonConnectError
from ..models import *
from ..provider.session import BridgeSession, SessionCrypto
from ..storage import IStorage


class HTTPBridge:
    SSE_PATH = "events"
    POST_PATH = "message"
    DEFAULT_TTL = 300

    def __init__(
            self,
            storage: IStorage,
            bridge_url: str,
            on_status_changed: Callable[..., Awaitable],
            api_tokens: Dict[str, str],
    ) -> None:
        self.storage = storage
        self.bridge_url = bridge_url

        self._on_status_changed = on_status_changed
        self._api_token = self.__get_api_token(api_tokens)

        self.session = BridgeSession()
        self.session.bridge_url = bridge_url

        self._is_closed: bool = False
        self._event_task: Optional[asyncio.Task] = None
        self._pending_requests: Dict[int, asyncio.Future] = {}
        self._client_session: Optional[aiohttp.ClientSession] = None

    def __get_api_token(self, api_tokens: Dict[str, str]) -> Optional[str]:
        for api_name, api_token in api_tokens.items():
            if api_name in self.bridge_url:
                return api_token
        return None

    def __build_post_url(self, to: str, topic: Optional[str] = None, ttl: Optional[int] = None) -> str:
        params = {
            "client_id": self.session.session_crypto.session_id,
            "to": to,
            "ttl": ttl or self.DEFAULT_TTL,
            "topic": topic,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self.__build_url(self.POST_PATH, params)

    def __build_sse_url(self, last_event_id: Optional[str] = None) -> str:
        params = {"client_id": self.session.session_crypto.session_id}
        if last_event_id:
            params["last_event_id"] = last_event_id
        return self.__build_url(self.SSE_PATH, params)

    def __build_url(self, path: str, params: dict) -> str:
        query_string = urlencode(params)
        return f"{self.bridge_url}/{path}?{query_string}"

    @staticmethod
    def __is_telegram_url(url: str) -> bool:
        return "tg" in url or "t.me" in url

    @staticmethod
    def __encode_telegram_params(params: str) -> str:
        startapp = (
                "tonconnect-"
                + params
                .replace("+", "")
                .replace(".", "%2E")
                .replace("-", "%2D")
                .replace("_", "%5F")
                .replace("=", "__")
                .replace("&", "-")
                .replace("%", "--")
                .replace(":", "--3A")
                .replace("/", "--2F")
        )
        return f"startapp={startapp}"

    @staticmethod
    def __convert_to_direct_link(universal_url: str) -> str:
        parsed = urlparse(universal_url)
        query_dict = parse_qs(parsed.query)

        if query_dict.pop("attach", None) is not None:
            new_path = parsed.path.rstrip("/")
            if not new_path.endswith("/start"):
                new_path += "/start"
            parsed = parsed._replace(path=new_path)

        new_query = urlencode(query_dict, doseq=True)
        parsed = parsed._replace(query=new_query)
        return parsed.geturl()

    async def _update_session(self, event: Dict[str, Any], wallet_public_key: str) -> None:
        self.session.wallet_public_key = wallet_public_key

        connection = {
            "type": "http",
            "session": self.session.get_dict(),
            "last_wallet_event_id": int(event.get("id", 0)),
            "connect_event": event,
            "next_rpc_request_id": 0,
        }
        await self.storage.set_item(IStorage.KEY_CONNECTION, json.dumps(connection))

    async def _cleanup_session(self, resolve_future: asyncio.Future) -> None:
        try:
            await self.remove_session()
            if not resolve_future.done():
                resolve_future.set_result(True)
        except Exception as err:
            if not resolve_future.done():
                resolve_future.set_exception(err)

    async def _handle_incoming_message(self, incoming_message: Dict[str, Any]) -> None:
        decrypted_message = self.session.session_crypto.decrypt(
            message=incoming_message["message"],
            sender_pub_key=incoming_message["from"],
        )
        message_data = json.loads(decrypted_message)

        event_id = int(message_data.get("id"))
        event_name = message_data.get("event")
        await self.storage.set_item(IStorage.KEY_LAST_EVENT_ID, str(event_id))

        connection = await self.get_stored_connection_data()
        last_event_id = int(connection.get("last_wallet_event_id", 0))

        if event_name is None:
            resolve = self._pending_requests.get(event_id)
            if resolve is None:
                return
            if not resolve.done():
                resolve.set_result(message_data)
            del self._pending_requests[event_id]
            return

        if event_id is not None:
            if event_id <= last_event_id:
                return
            if event_name != Event.CONNECT:
                connection["last_wallet_event_id"] = int(event_id)
                await self.storage.set_item(IStorage.KEY_CONNECTION, json.dumps(connection))

        if event_name == Event.CONNECT:
            await self._update_session(message_data, incoming_message["from"])
        elif event_name == Event.DISCONNECT:
            await self.remove_session()
        await self._on_status_changed(message_data)

    async def _subscribe_to_events(self, url: str) -> None:
        if not self._client_session:
            self._client_session = aiohttp.ClientSession()

        try:
            headers = {"Authorization": f"Bearer {self._api_token}"} if self._api_token else {}
            async with self._client_session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise TonConnectError(f"Failed to connect to bridge: {response.status}")

                async for line in response.content:
                    if self._is_closed:
                        break
                    decoded_line = line.decode().strip()
                    if decoded_line.startswith("data:"):
                        raw_json = decoded_line[5:].strip()
                        if not raw_json:
                            continue
                        try:
                            incoming_data = json.loads(raw_json)
                            await self._handle_incoming_message(incoming_data)
                        except json.JSONDecodeError:
                            continue
        except (aiohttp.ClientError, asyncio.CancelledError) as e:
            if isinstance(e, aiohttp.ClientError):
                raise TonConnectError(f"HTTP Client Error: {e}") from e
            elif isinstance(e, asyncio.CancelledError):
                pass
        except RuntimeError:
            try:
                await self.restore_connection()
            except TonConnectError:
                await self._on_status_changed(SendDisconnectRequest().to_dict())
                await self.remove_session()
        finally:
            await self.pause_sse()

    async def _send(
            self,
            request: str,
            receiver_public_key: str,
            topic: Optional[str] = None,
            ttl: Optional[int] = None,
    ) -> None:
        url = self.__build_post_url(receiver_public_key, topic, ttl)
        headers = {"Content-type": "text/plain;charset=UTF-8"}
        if self._api_token:
            headers["Authorization"] = f"Bearer {self._api_token}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=request, headers=headers) as resp:
                    if resp.status != 200:
                        raise TonConnectError(f"Failed to send message: {resp.status}")
            except aiohttp.ClientError as e:
                raise TonConnectError(f"HTTP Client Error: {e}")

    async def start_sse(self) -> None:
        if self._is_closed:
            return

        last_event_id = await self.storage.get_item(IStorage.KEY_LAST_EVENT_ID)
        url = self.__build_sse_url(last_event_id)

        if self._event_task:
            self._event_task.cancel()
            try:
                await self._event_task
            except asyncio.CancelledError:
                pass

        loop = asyncio.get_running_loop()
        self._event_task = loop.create_task(self._subscribe_to_events(url))

    async def pause_sse(self) -> None:
        if self._client_session:
            await self._client_session.close()
            self._client_session = None

        if self._event_task and not self._event_task.done():
            self._event_task.cancel()
            try:
                await self._event_task
            except asyncio.CancelledError:
                pass

        self._event_task = None

    async def send_request(
            self,
            request: Request,
            connection: Dict[str, Any],
            stored_request_id: int,
            on_request_sent: Optional[Callable] = None,
    ) -> Any:
        if not self.session or not self.session.wallet_public_key:
            raise TonConnectError("Trying to send a request without an active session.")

        connection["next_rpc_request_id"] = str(stored_request_id + 1)
        await self.storage.set_item(IStorage.KEY_CONNECTION, json.dumps(connection))

        request.id = stored_request_id
        message = json.dumps(request.to_dict())

        encoded_request = self.session.session_crypto.encrypt(
            message=message,
            receiver_pub_key=self.session.wallet_public_key,
        )
        await self._send(
            request=encoded_request,
            receiver_public_key=self.session.wallet_public_key,
            topic=request.method,
        )

        loop = asyncio.get_running_loop()
        resolve = loop.create_future()
        self._pending_requests[stored_request_id] = resolve
        if on_request_sent is not None:
            on_request_sent(resolve)

        return await resolve

    async def send_request_with_cleanup(
            self,
            request: Any,
            connection: Dict[str, Any],
            rpc_request_id: int,
            timeout: float
    ) -> None:
        loop = asyncio.get_running_loop()
        disconnect_future = loop.create_future()

        def on_request_sent(resolve: asyncio.Future) -> None:
            loop.create_task(self._cleanup_session(resolve))

        try:
            await asyncio.wait_for(
                self.send_request(
                    request=request,
                    connection=connection,
                    stored_request_id=rpc_request_id,
                    on_request_sent=on_request_sent
                ),
                timeout=timeout
            )
        except Exception:
            if not disconnect_future.done():
                disconnect_future.set_result(True)
            raise

    async def get_stored_connection_data(self) -> Dict[str, Any]:
        connection = await self.storage.get_item(IStorage.KEY_CONNECTION, "{}")
        return json.loads(connection)  # type: ignore

    def generate_universal_url(
            self,
            request: Dict[str, Any],
            universal_url: str,
            redirect_url: str,
    ) -> str:
        version = 2
        session_id = self.session.session_crypto.session_id
        request_safe = quote_plus(json.dumps(request, separators=(",", ":")))
        query_params = f"v={version}&id={session_id}&r={request_safe}&ret={redirect_url}"

        if self.__is_telegram_url(universal_url):
            universal_url = self.__convert_to_direct_link(universal_url)
            query_params = self.__encode_telegram_params(query_params)
            return f"{universal_url}?{query_params}"

        return f"{universal_url}?{query_params}"

    async def connect(
            self,
            request: SendConnectRequest,
            universal_url: str,
            redirect_url: str = "back",
    ) -> str:
        await self.close_connection()

        session_crypto = SessionCrypto()
        self.session.bridge_url = self.bridge_url
        self.session.session_crypto = session_crypto

        await self.start_sse()
        return self.generate_universal_url(request.to_dict(), universal_url, redirect_url)

    async def restore_connection(self) -> WalletInfo:
        stored_connection = await self.storage.get_item(IStorage.KEY_CONNECTION)
        if not stored_connection:
            raise TonConnectError("Restore failed: no connection data found in storage.")

        connection = json.loads(stored_connection)
        if "session" not in connection:
            raise TonConnectError("Restore failed: no session data found in storage.")

        self.session = BridgeSession(stored=connection["session"])
        if self.session.bridge_url is None:
            raise TonConnectError("Restore failed: no bridge_url found in storage.")
        self.bridge_url = self.session.bridge_url

        connect_event = connection.get("connect_event")
        payload = connect_event.get("payload") if connect_event else None
        if payload is None:
            raise TonConnectError("Failed to restore connection: no payload found in stored response.")

        await self.start_sse()
        return WalletInfo.from_payload(payload)

    async def close_connection(self) -> None:
        await self.pause_sse()
        self.session = BridgeSession()
        self._pending_requests.clear()

    async def remove_session(self) -> None:
        await self.close_connection()
        await self.storage.remove_item(IStorage.KEY_CONNECTION)
        await self.storage.remove_item(IStorage.KEY_LAST_EVENT_ID)

    async def close(self) -> None:
        self._is_closed = True
        await self.close_connection()
