"""Top-level package for the ``synergy_phi`` library."""

from .metrics import (
    expanded_being_seen_quotient,
    intrinsic_resonance,
    coherence,
    dyadic_synergy_index,
    being_seen_quotient,
)
from .logger import DeltaRaLogger
from .powit import (
    KeyPair,
    Ledger,
    Receipt,
    generate_keypair,
    turn_digest,
    sign_receipt,
    verify_receipt,
)

__all__ = [
    "expanded_being_seen_quotient",
    "intrinsic_resonance",
    "coherence",
    "dyadic_synergy_index",
    "being_seen_quotient",
    "DeltaRaLogger",
    "KeyPair",
    "Ledger",
    "Receipt",
    "generate_keypair",
    "turn_digest",
    "sign_receipt",
    "verify_receipt",
]


def hello() -> str:
    """Return a friendly greeting."""

    return "Hello from synergy_phi!"
