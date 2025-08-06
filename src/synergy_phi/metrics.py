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
from typing import Sequence, List

__all__ = [
    "expanded_being_seen_quotient",
    "intrinsic_resonance",
    "coherence",
]


def _cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    """Return cosine similarity between vectors ``a`` and ``b``."""

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        raise ValueError("cosine similarity undefined for zero-length vectors")
    return dot / (norm_a * norm_b)


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
