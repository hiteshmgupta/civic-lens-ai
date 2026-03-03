"""
Tests for the Python Controversy Index Calculator.
Mirrors the Java ControversyCalculatorTest for consistency.
"""
import math
import pytest
from models.controversy import (
    vote_polarity,
    sentiment_variance,
    sentiment_mean,
    stance_entropy,
    engagement_intensity,
    controversy_score,
    controversy_label,
)


# ---------------------------------------------------------------
# Vote Polarity: P = 1 − |U − D| / (U + D) ∈ [0,1]
# ---------------------------------------------------------------

class TestVotePolarity:
    def test_even_split_returns_one(self):
        assert vote_polarity(50, 50) == pytest.approx(1.0)

    def test_unanimous_returns_zero(self):
        assert vote_polarity(100, 0) == pytest.approx(0.0)
        assert vote_polarity(0, 100) == pytest.approx(0.0)

    def test_no_votes_returns_zero(self):
        assert vote_polarity(0, 0) == pytest.approx(0.0)

    def test_typical_distribution(self):
        # P = 1 - |60-40|/100 = 0.8
        assert vote_polarity(60, 40) == pytest.approx(0.8)


# ---------------------------------------------------------------
# Sentiment Variance: S = σ² ∈ [0,1]
# ---------------------------------------------------------------

class TestSentimentVariance:
    def test_empty_returns_zero(self):
        assert sentiment_variance([]) == pytest.approx(0.0)

    def test_uniform_returns_zero(self):
        assert sentiment_variance([0.5, 0.5, 0.5]) == pytest.approx(0.0)

    def test_mixed_returns_positive(self):
        # scores: -1, 1 → mean=0, variance = 1.0
        assert sentiment_variance([-1.0, 1.0]) == pytest.approx(1.0)

    def test_bounded_to_unit(self):
        s = sentiment_variance([-1.0, 1.0, -1.0, 1.0])
        assert 0 <= s <= 1.0


# ---------------------------------------------------------------
# Sentiment Mean
# ---------------------------------------------------------------

class TestSentimentMean:
    def test_empty_returns_zero(self):
        assert sentiment_mean([]) == pytest.approx(0.0)

    def test_typical(self):
        assert sentiment_mean([0.0, 1.0]) == pytest.approx(0.5)


# ---------------------------------------------------------------
# Stance Entropy: D = H / log(K) ∈ [0,1]
# ---------------------------------------------------------------

class TestStanceEntropy:
    def test_even_distribution_returns_one(self):
        counts = {"support": 25, "oppose": 25, "suggestion": 25, "neutral": 25}
        assert stance_entropy(counts) == pytest.approx(1.0)

    def test_single_category_returns_zero(self):
        assert stance_entropy({"support": 100}) == pytest.approx(0.0)

    def test_empty_returns_zero(self):
        assert stance_entropy({}) == pytest.approx(0.0)

    def test_skewed_between_zero_and_one(self):
        counts = {"support": 90, "oppose": 10}
        d = stance_entropy(counts)
        assert 0 < d < 1.0


# ---------------------------------------------------------------
# Engagement Intensity: E = log(1+n) / log(1+n_max) ∈ [0,1]
# ---------------------------------------------------------------

class TestEngagementIntensity:
    def test_zero_comments(self):
        assert engagement_intensity(0, 100) == pytest.approx(0.0)

    def test_max_comments(self):
        assert engagement_intensity(100, 100) == pytest.approx(1.0)

    def test_zero_max(self):
        assert engagement_intensity(50, 0) == pytest.approx(0.0)

    def test_typical_between_zero_and_one(self):
        e = engagement_intensity(50, 200)
        assert 0 < e < 1.0


# ---------------------------------------------------------------
# Controversy Score: C(a) = S · P · D · √E ∈ [0,1]
# ---------------------------------------------------------------

class TestControversyScore:
    def test_zero_component(self):
        assert controversy_score(0.5, 0.0, 0.5, 0.5) == pytest.approx(0.0)
        assert controversy_score(0.0, 0.5, 0.5, 0.5) == pytest.approx(0.0)

    def test_all_max(self):
        assert controversy_score(1.0, 1.0, 1.0, 1.0) == pytest.approx(1.0)

    def test_clamped_to_unit(self):
        c = controversy_score(0.5, 0.8, 0.7, 0.6)
        assert 0 <= c <= 1.0


# ---------------------------------------------------------------
# Controversy Label
# ---------------------------------------------------------------

class TestControversyLabel:
    def test_all_thresholds(self):
        assert controversy_label(0.0) == "Low"
        assert controversy_label(0.24) == "Low"
        assert controversy_label(0.25) == "Moderate"
        assert controversy_label(0.49) == "Moderate"
        assert controversy_label(0.50) == "High"
        assert controversy_label(0.74) == "High"
        assert controversy_label(0.75) == "Extreme"
        assert controversy_label(1.0) == "Extreme"
