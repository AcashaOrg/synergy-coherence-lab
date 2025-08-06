import pytest

from synergy_phi.metrics import (
    expanded_being_seen_quotient,
    intrinsic_resonance,
    coherence,
)


def test_expanded_being_seen_quotient():
    affirmations = [7, 6, 7]
    embeddings = [
        [1.0, 0.0],
        [0.8, 0.2],
        [0.9, 0.1],
    ]
    baseline = [1.0, 0.0]
    result = expanded_being_seen_quotient(affirmations, embeddings, baseline)
    assert result == pytest.approx(0.941, rel=1e-3)


def test_intrinsic_resonance():
    aligned = [-1.0, -0.5, -1.2]
    baseline = [-1.5, -0.6, -1.4]
    result = intrinsic_resonance(aligned, baseline)
    assert result == pytest.approx(0.2667, rel=1e-3)


def test_coherence():
    embeddings = [
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
    ]
    result = coherence(embeddings)
    assert result[0] == pytest.approx(0.0, abs=1e-6)
    assert result[1] == pytest.approx(0.70710678, rel=1e-6)
