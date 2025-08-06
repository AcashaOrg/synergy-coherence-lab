"""Minimal Proof-of-Witness (PoWit) protocol components.

This module implements a small subset of the protocol sketched in the
R-CAT thesis.  It provides utilities for key generation, SHA-256 turn
Digests, signing and verifying receipts, and an in-memory append-only
ledger interface.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import List

__all__ = [
    "KeyPair",
    "generate_keypair",
    "turn_digest",
    "sign_receipt",
    "verify_receipt",
    "Receipt",
    "Ledger",
]


@dataclass
class KeyPair:
    private_key: bytes
    public_key: bytes


def generate_keypair() -> KeyPair:
    """Generate a new signing key pair."""

    priv = secrets.token_bytes(32)
    pub = hashlib.sha256(priv).digest()
    return KeyPair(priv, pub)


def turn_digest(payload: bytes) -> str:
    """Return the SHA-256 hex digest for ``payload``."""

    return hashlib.sha256(payload).hexdigest()


def sign_receipt(message: bytes, key: KeyPair) -> bytes:
    """Create an HMAC-SHA256 signature for ``message`` using ``key``."""

    return hmac.new(key.private_key, message, hashlib.sha256).digest()


def verify_receipt(message: bytes, signature: bytes, key: KeyPair) -> bool:
    """Verify an HMAC-SHA256 ``signature`` for ``message``."""

    expected = hmac.new(key.private_key, message, hashlib.sha256).digest()
    return hmac.compare_digest(expected, signature)


@dataclass
class Receipt:
    public_key: bytes
    digest: str
    signature: bytes


class Ledger:
    """Simple in-memory append-only ledger."""

    def __init__(self) -> None:
        self.entries: List[Receipt] = []

    def commit(self, receipt: Receipt) -> None:
        self.entries.append(receipt)
