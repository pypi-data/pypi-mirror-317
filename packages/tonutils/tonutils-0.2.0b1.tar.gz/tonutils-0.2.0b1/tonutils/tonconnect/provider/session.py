import base64
from typing import Optional, Any, Dict, Union

from nacl.encoding import HexEncoder
from nacl.public import PublicKey, PrivateKey, Box


class SessionCrypto:

    def __init__(self, private_key: Optional[Union[str, bytes]] = None) -> None:
        self.private_key = PrivateKey(private_key, HexEncoder) if private_key else PrivateKey.generate()
        self.session_id = self.private_key.public_key.encode().hex()

    def encrypt(self, message: str, receiver_pub_key: Union[str, bytes]) -> str:
        receiver_pub_key = PublicKey(receiver_pub_key, encoder=HexEncoder)
        box = Box(self.private_key, receiver_pub_key)

        message_bytes = message.encode()
        encrypted = box.encrypt(message_bytes)

        return base64.b64encode(encrypted).decode()

    def decrypt(self, message: str, sender_pub_key: Union[str, bytes]) -> str:
        encrypted_message = base64.b64decode(message)

        sender_pub_key = PublicKey(sender_pub_key, encoder=HexEncoder)
        box = Box(self.private_key, sender_pub_key)

        decrypted = box.decrypt(encrypted_message)
        return decrypted.decode()


class BridgeSession:

    def __init__(self, stored: Optional[Dict[str, Any]] = None) -> None:
        stored = stored or {}
        self.session_crypto = SessionCrypto(private_key=stored.get("session_private_key"))
        self.wallet_public_key = stored.get("wallet_public_key")
        self.bridge_url = stored.get("bridge_url")

    def get_dict(self) -> Dict[str, Any]:
        session_private_key = (
            self.session_crypto.private_key.encode().hex()
            if self.session_crypto.private_key else
            None
        )
        return {
            "session_private_key": session_private_key,
            "wallet_public_key": self.wallet_public_key,
            "bridge_url": self.bridge_url
        }
