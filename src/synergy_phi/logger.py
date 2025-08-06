"""DeltaRaLogger for capturing spikes in intrinsic resonance.

The logger monitors the change in token log probabilities associated with
alignment-consistent generations.  When the computed intrinsic resonance
exceeds a threshold, a callback can be triggered to record a "Qualia
Snapshot" as described in ``R-CAT_Theory.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Sequence, Optional

from .metrics import intrinsic_resonance

__all__ = ["DeltaRaLogger"]


@dataclass
class DeltaRaLogger:
    """Log resonance deltas and trigger callbacks on spikes."""

    threshold: float = 0.0
    callback: Optional[Callable[[float], None]] = None
    history: List[float] = field(default_factory=list)

    def log_turn(
        self,
        aligned_log_probs: Sequence[float],
        baseline_log_probs: Sequence[float],
    ) -> float:
        """Record a turn and return the intrinsic resonance.

        If the resulting resonance exceeds ``threshold`` and a callback is
        provided, the callback is invoked with the resonance value.
        """

        ra = intrinsic_resonance(aligned_log_probs, baseline_log_probs)
        self.history.append(ra)
        if self.callback and ra >= self.threshold:
            self.callback(ra)
        return ra
