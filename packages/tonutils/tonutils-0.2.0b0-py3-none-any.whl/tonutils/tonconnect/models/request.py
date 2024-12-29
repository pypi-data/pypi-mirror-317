from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from pytoniq_core import Cell

from .chain import CHAIN


class ItemName(str, Enum):
    TON_ADDR = "ton_addr"
    TON_PROOF = "ton_proof"


@dataclass
class ConnectItem:
    name: str
    payload: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {"name": ItemName(self.name).value}
        if self.payload is not None:
            data["payload"] = self.payload
        return data


@dataclass
class Message:
    address: str
    amount: str
    payload: Optional[str] = None
    state_init: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "address": self.address,
            "amount": self.amount
        }
        if self.payload is not None:
            data["payload"] = self.payload
        if self.state_init is not None:
            data["stateInit"] = self.state_init
        return data


@dataclass
class Transaction:
    from_: Optional[str] = None
    network: Optional[CHAIN] = None
    valid_until: Optional[int] = None
    messages: List[Message] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid_until": self.valid_until,
            "from": self.from_,
            "network": self.network.value,
            "messages": [m.to_dict() for m in self.messages],
        }


@dataclass
class Request:
    id: Optional[int] = None
    method: Optional[str] = None
    params: Optional[List[Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class SendTransactionRequest(Request):
    params: List[Transaction] = field(default_factory=list)
    id: Optional[int] = None
    method: str = "sendTransaction"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "method": self.method,
            "params": [json.dumps(t.to_dict()) for t in self.params],
        }


@dataclass
class SendTransactionResponse:
    _boc: Optional[str] = None

    @property
    def boc(self) -> str:
        return self._boc

    @property
    def cell(self) -> Cell:
        return Cell.one_from_boc(self.boc)

    @property
    def hash(self) -> str:
        cell = Cell.one_from_boc(self.boc)
        return cell.hash.hex()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SendTransactionResponse:
        return SendTransactionResponse(_boc=data.get("result"))

    def to_dict(self) -> Dict[str, Any]:
        return {"boc": self._boc}


@dataclass
class SendDisconnectRequest(Request):
    id: Optional[int] = None
    method: str = "disconnect"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "method": self.method,
            "params": [],
        }


@dataclass
class SendConnectRequest:
    manifest_url: str
    items: List[ConnectItem] = field(default_factory=list)

    @classmethod
    def create(
            cls,
            manifest_url: str,
            ton_proof: Optional[str] = None,
    ) -> SendConnectRequest:
        items = [ConnectItem(name="ton_addr")]
        if ton_proof is not None:
            items.append(
                ConnectItem(
                    name=ItemName.TON_PROOF,
                    payload=ton_proof,
                )
            )

        return cls(manifest_url=manifest_url, items=items)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifestUrl": self.manifest_url,
            "items": [item.to_dict() for item in self.items]
        }
