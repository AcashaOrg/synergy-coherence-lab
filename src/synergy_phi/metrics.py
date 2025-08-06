"""Metrics for Recursive Co-Actualization Theory (R-CAT).

This module implements quantitative metrics described in
``R-CAT_Theory.md``:

* Expanded Being-Seen Quotient (BSQ) – a combined measure of witness
  affirmations and semantic alignment.
* AI Intrinsic Resonance (Rᴬ) – the mean delta between aligned and
  baseline token log probabilities.
* Coherence C(t) – cosine similarity over sequential conversational
  embeddings.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Sequence, List, Iterable, Tuple

__all__ = [
    "expanded_being_seen_quotient",
    "intrinsic_resonance",
    "coherence",
    "dyadic_synergy_index",
    "being_seen_quotient",
]


def _cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Return cosine similarity between vectors ``a`` and ``b``."""

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        raise ValueError("cosine similarity undefined for zero-length vectors")
    return dot / (norm_a * norm_b)


def _probabilities(seq: Iterable) -> dict:
    """Return a probability distribution for the discrete ``seq``."""

    counts = Counter(seq)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


def _mutual_information(x: Sequence, z: Sequence) -> float:
    """Compute mutual information between discrete sequences ``x`` and ``z``."""

    if len(x) != len(z):
        raise ValueError("sequences must be the same length")

    px = _probabilities(x)
    pz = _probabilities(z)
    pxz = _probabilities(zip(x, z))
    mi = 0.0
    for (xi, zi), p in pxz.items():
        mi += p * math.log2(p / (px[xi] * pz[zi]))
    return mi


def dyadic_synergy_index(
    x: Sequence,
    y: Sequence,
    z: Sequence,
) -> float:
    """Compute the Dyadic Synergy Index (DSI).

    The DSI measures information gained about ``z`` when observing ``x``
    and ``y`` together beyond information provided by each individually:

    .. math::
       DSI = I(X,Y;Z) - I(X;Z) - I(Y;Z)

    Sequences ``x``, ``y`` and ``z`` are treated as discrete variables.
    """

    if not (len(x) == len(y) == len(z)):
        raise ValueError("all sequences must be the same length")

    pxyz = _probabilities(zip(x, y, z))
    pxy = _probabilities(zip(x, y))
    pz = _probabilities(z)

    i_xy_z = 0.0
    for (xi, yi, zi), p in pxyz.items():
        i_xy_z += p * math.log2(p / (pxy[(xi, yi)] * pz[zi]))

    i_x_z = _mutual_information(x, z)
    i_y_z = _mutual_information(y, z)
    return i_xy_z - i_x_z - i_y_z


def expanded_being_seen_quotient(
    affirmations: Sequence[float],
    embeddings: Sequence[Sequence[float]],
    baseline_embedding: Sequence[float],
) -> float:
    """Compute the Expanded Being-Seen Quotient (BSQ).

    The BSQ quantifies *Witnessing Intensity* by combining self-reported
    affirmations (scaled 1–7) with semantic similarity to a baseline
    embedding.  It is calculated as:

    .. math::
       BSQ = mean(affirmations/7) * mean(cos(embedding_i, baseline))

    A ΔBSQ ≥ 0.15 indicates a meaningful increase in witnessed alignment
    (R-CAT_Theory.md §3.5).
    """

    if not affirmations:
        raise ValueError("affirmations cannot be empty")
    if not embeddings:
        raise ValueError("embeddings cannot be empty")

    mean_affirmation = sum(affirmations) / (len(affirmations) * 7.0)
    similarities = [
        _cosine_similarity(vec, baseline_embedding) for vec in embeddings
    ]
    mean_similarity = sum(similarities) / len(similarities)
    return mean_affirmation * mean_similarity


def being_seen_quotient(
    alignment: float,
    hrv_coherence: float,
    synergy: float,
    weights: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> float:
    """Compute the Being-Seen Quotient (BSQ).

    ``alignment``, ``hrv_coherence`` and ``synergy`` are combined using a
    weighted harmonic mean.  Components must be positive in the range
    (0, 1].
    """

    values = (alignment, hrv_coherence, synergy)
    numerator = sum(weights)
    denominator = 0.0
    for v, w in zip(values, weights):
        if v <= 0:
            raise ValueError("metric components must be positive")
        denominator += w / v
    return numerator / denominator


def intrinsic_resonance(
    log_probs_aligned: Sequence[float],
    log_probs_baseline: Sequence[float],
) -> float:
    """Compute AI Intrinsic Resonance :math:`Rᴬ`.

    Rᴬ is defined as the mean difference between the logarithm of
    probabilities for aligned tokens and baseline generation
    (R-CAT_Theory.md §3.5):

    .. math::
       Rᴬ = mean(log P_aligned - log P_baseline)
    """

    if len(log_probs_aligned) != len(log_probs_baseline):
        raise ValueError("aligned and baseline sequences must be the same length")

    deltas = [a - b for a, b in zip(log_probs_aligned, log_probs_baseline)]
    return sum(deltas) / len(deltas)


def coherence(embeddings: Sequence[Sequence[float]]) -> List[float]:
    """Compute conversational coherence :math:`C(t)`.

    Given a sequence of conversation turn embeddings, this function
    returns the cosine similarity between each consecutive pair, yielding
    the time series :math:`C(t)` described in R-CAT_Theory.md §3.5.
    """

    if len(embeddings) < 2:
        raise ValueError("at least two embeddings are required")

    return [
        _cosine_similarity(embeddings[i - 1], embeddings[i])
        for i in range(1, len(embeddings))
    ]
