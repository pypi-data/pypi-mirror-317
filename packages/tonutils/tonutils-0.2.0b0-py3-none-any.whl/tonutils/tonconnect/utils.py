import logging
import time
from secrets import token_bytes
from typing import Optional

from .models import WalletInfo


def generate_proof(ttl: Optional[int] = None) -> str:
    if ttl is None:
        from .connector import Connector
        ttl = Connector.DISCONNECT_TIMEOUT

    random_bytes = token_bytes(8)
    expire_time = int(time.time()) + ttl

    payload = bytearray(random_bytes)
    payload.extend(expire_time.to_bytes(8, "big"))

    return payload.hex()


def verify_proof(proof_hex: str, wallet_info: WalletInfo) -> bool:
    if len(proof_hex) < 32:
        return False

    if not wallet_info.verify_proof(proof_hex):
        return False

    try:
        expire_time = int(proof_hex[16:32], 16)
    except ValueError:
        logging.warning("Invalid proof format: can't parse timestamp.")
        return False

    if time.time() > expire_time:
        logging.warning("Proof is expired.")
        return False

    return True
