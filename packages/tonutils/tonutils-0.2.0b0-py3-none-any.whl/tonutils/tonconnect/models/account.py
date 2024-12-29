from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from pytoniq_core import Address

from .chain import CHAIN
from ..exceptions import TonConnectError


@dataclass
class Account:
    address: Address
    chain: CHAIN
    wallet_state_init: str
    public_key: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Account:
        if "address" not in data:
            raise TonConnectError("address not contains in ton_addr")

        return cls(
            address=Address(data["address"]),
            chain=CHAIN(data["network"]),
            wallet_state_init=data["walletStateInit"],
            public_key=data.get("publicKey"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "address": self.address,
            "network": self.chain.value,
            "walletStateInit": self.wallet_state_init,
            "publicKey": self.public_key,
        }
