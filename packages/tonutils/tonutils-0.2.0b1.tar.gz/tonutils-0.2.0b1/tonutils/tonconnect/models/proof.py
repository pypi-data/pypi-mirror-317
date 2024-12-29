from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..exceptions import TonConnectError


@dataclass
class TonProof:
    timestamp: int
    domain_len: int
    domain_val: str
    payload: str
    signature: bytes

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TonProof:
        proof = data.get("proof")
        if not proof:
            raise TonConnectError("proof not contains in ton_proof")

        timestamp = proof.get("timestamp")
        domain_data = proof.get("domain") or {}
        domain_len = domain_data.get("lengthBytes")
        if domain_len is None:
            raise TonConnectError("domain length not contains in ton_proof")
        domain_val = domain_data.get("value")
        if domain_val is None:
            raise TonConnectError("domain value not contains in ton_proof")
        payload = proof.get("payload")

        signature_base64: Optional[str] = proof.get("signature")
        signature = base64.b64decode(signature_base64) if signature_base64 else b""

        return cls(
            timestamp=timestamp,
            domain_len=domain_len,
            domain_val=domain_val,
            payload=payload,
            signature=signature,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "domain": {
                "lengthBytes": self.domain_len,
                "value": self.domain_val,
            },
            "payload": self.payload,
            "signature": self.signature,
        }
