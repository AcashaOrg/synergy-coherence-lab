import pytest

from synergy_phi.logger import DeltaRaLogger
from synergy_phi.powit import (
    Ledger,
    Receipt,
    generate_keypair,
    turn_digest,
    sign_receipt,
    verify_receipt,
)


def test_delta_ra_logger_triggers_callback():
    triggered = []

    def cb(value: float) -> None:
        triggered.append(value)

    logger = DeltaRaLogger(threshold=0.1, callback=cb)
    ra = logger.log_turn([-0.5, -0.4], [-1.0, -0.9])
    assert ra > 0.1
    assert triggered and triggered[0] == ra


def test_powit_sign_and_commit():
    key = generate_keypair()
    digest = turn_digest(b"hello")
    signature = sign_receipt(digest.encode(), key)
    assert verify_receipt(digest.encode(), signature, key)

    ledger = Ledger()
    receipt = Receipt(public_key=key.public_key, digest=digest, signature=signature)
    ledger.commit(receipt)
    assert ledger.entries[0].digest == digest
