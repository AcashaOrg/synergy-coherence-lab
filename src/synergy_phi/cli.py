"""Command line interface for ``synergy_phi``."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import hello
from .metrics import (
    coherence,
    expanded_being_seen_quotient,
    intrinsic_resonance,
)


def _load_json(path: str) -> Any:
    with open(Path(path), "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    """Entry point for the ``synergy-phi`` command."""

    parser = argparse.ArgumentParser(description="synergy_phi metrics")
    sub = parser.add_subparsers(dest="command")

    p_bsq = sub.add_parser("bsq", help="Compute Expanded Being-Seen Quotient")
    p_bsq.add_argument("file", help="JSON file with affirmations, embeddings, baseline")

    p_ra = sub.add_parser("ra", help="Compute AI Intrinsic Resonance")
    p_ra.add_argument("file", help="JSON file with aligned and baseline log probs")

    p_c = sub.add_parser("coherence", help="Compute conversational coherence")
    p_c.add_argument("file", help="JSON file with embeddings list")

    args = parser.parse_args()

    if args.command == "bsq":
        data = _load_json(args.file)
        result = expanded_being_seen_quotient(
            data["affirmations"], data["embeddings"], data["baseline"]
        )
        print(result)
    elif args.command == "ra":
        data = _load_json(args.file)
        result = intrinsic_resonance(data["aligned"], data["baseline"])
        print(result)
    elif args.command == "coherence":
        data = _load_json(args.file)
        result = coherence(data["embeddings"])
        print(json.dumps(result))
    else:
        print(hello())

