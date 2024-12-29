from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from nacl.signing import VerifyKey

from ..exceptions import TonConnectError
from ..models import Account, DeviceInfo, TonProof


@dataclass
class WalletApp:
    app_name: str
    name: str
    image: str
    bridge_url: str
    tondns: Optional[str] = None
    about_url: Optional[str] = None
    universal_url: Optional[str] = None
    deep_link: Optional[str] = None
    platforms: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WalletApp:
        return cls(
            app_name=data["app_name"],
            name=data["name"],
            image=data["image"],
            bridge_url=data["bridge_url"],
            tondns=data.get("tondns"),
            about_url=data.get("about_url"),
            universal_url=data.get("universal_url"),
            deep_link=data.get("deepLink"),
            platforms=data.get("platforms"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app_name": self.app_name,
            "name": self.name,
            "image": self.image,
            "bridge_url": self.bridge_url,
            "tondns": self.tondns,
            "about_url": self.about_url,
            "universal_url": self.universal_url,
            "deepLink": self.deep_link,
            "platforms": self.platforms,
        }


@dataclass
class WalletInfo:
    device: Optional[DeviceInfo] = None
    provider: str = field(default="http")
    account: Optional[Account] = None
    ton_proof: Optional[TonProof] = None

    def verify_proof(self, src_payload: Optional[str] = None) -> bool:
        if self.ton_proof is None or self.account is None:
            return False

        wc, whash = self.account.address.wc, self.account.address.hash_part

        message = bytearray()
        message.extend("ton-proof-item-v2/".encode())
        message.extend(int(wc, 10).to_bytes(4, "little"))
        message.extend(whash)
        message.extend(self.ton_proof.domain_len.to_bytes(4, "little"))
        message.extend(self.ton_proof.domain_val.encode())
        message.extend(self.ton_proof.timestamp.to_bytes(8, "little"))

        message.extend((src_payload or self.ton_proof.payload).encode())

        signature_message = bytearray()
        signature_message.extend(bytes.fromhex("ffff"))
        signature_message.extend("ton-connect".encode())
        signature_message.extend(hashlib.sha256(message).digest())

        public_key = self.account.public_key
        if isinstance(public_key, str):
            try:
                public_key_bytes = bytes.fromhex(public_key)
            except ValueError:
                logging.debug("Public key is not a valid hex string.")
                return False
        elif isinstance(public_key, bytes):
            public_key_bytes = public_key
        else:
            logging.debug("Public key is neither str nor bytes.")
            return False

        try:
            verify_key = VerifyKey(public_key_bytes)
            verify_key.verify(
                hashlib.sha256(signature_message).digest(),
                self.ton_proof.signature,
            )
            logging.debug("Proof is ok!")
            return True
        except (Exception,):
            logging.debug("Proof is invalid!")
        return False

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> WalletInfo:
        items = payload.get("items")
        if not items:
            raise TonConnectError("items not contains in payload")

        wallet = cls()
        for item in items:
            item_name = item.pop("name")
            if item_name == "ton_addr":
                wallet.account = Account.from_dict(item)
            elif item_name == "ton_proof":
                wallet.ton_proof = TonProof.from_dict(item)

        if not wallet.account:
            raise TonConnectError("ton_addr not contains in items")

        device_info = payload.get("device")
        if device_info:
            wallet.device = DeviceInfo.from_dict(device_info)

        return wallet

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WalletInfo:
        device_data = data.get("device")
        account_data = data.get("account")
        ton_proof_data = data.get("ton_proof")

        device_obj = None
        if device_data is not None:
            device_obj = DeviceInfo.from_dict(device_data)

        account_obj = None
        if account_data is not None:
            account_obj = Account.from_dict(account_data)

        ton_proof_obj = None
        if ton_proof_data is not None:
            ton_proof_obj = TonProof.from_dict(ton_proof_data)

        return cls(
            device=device_obj,
            provider=data.get("provider", "http"),
            account=account_obj,
            ton_proof=ton_proof_obj,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device": self.device.to_dict() if self.device else None,
            "provider": self.provider,
            "account": self.account.to_dict() if self.account else None,
            "ton_proof": self.ton_proof.to_dict() if self.ton_proof else None,
        }
