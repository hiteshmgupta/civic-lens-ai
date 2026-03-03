"""
Controversy Index Calculator — Python implementation.
C(a) = S · P · D · √E
"""
import math
import logging

logger = logging.getLogger(__name__)


def vote_polarity(upvotes: int, downvotes: int) -> float:
    """P = 1 - |U - D| / (U + D) ∈ [0,1]"""
    total = upvotes + downvotes
    if total == 0:
        return 0.0
    return 1.0 - abs(upvotes - downvotes) / total


def sentiment_variance(scores: list[float]) -> float:
    """S = σ² of sentiment scores ∈ [0,1]"""
    if not scores:
        return 0.0
    n = len(scores)
    mean = sum(scores) / n
    var = sum((s - mean) ** 2 for s in scores) / n
    return min(var, 1.0)


def sentiment_mean(scores: list[float]) -> float:
    """Mean of sentiment scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def stance_entropy(stance_counts: dict) -> float:
    """D = H / log(K), normalized Shannon entropy ∈ [0,1]"""
    if not stance_counts:
        return 0.0
    counts = [v for v in stance_counts.values() if v > 0]
    K = len(counts)
    if K <= 1:
        return 0.0
    total = sum(counts)
    if total == 0:
        return 0.0
    H = -sum((c / total) * math.log(c / total) for c in counts)
    max_H = math.log(K)
    return H / max_H if max_H > 0 else 0.0


def engagement_intensity(n: int, n_max: int) -> float:
    """E = log(1+n) / log(1+n_max) ∈ [0,1]"""
    if n_max <= 0:
        return 0.0
    return math.log(1 + n) / math.log(1 + n_max)


def controversy_score(S: float, P: float, D: float, E: float) -> float:
    """C(a) = S · P · D · √E ∈ [0,1]"""
    return max(0.0, min(1.0, S * P * D * math.sqrt(E)))


def controversy_label(score: float) -> str:
    if score < 0.25:
        return "Low"
    elif score < 0.50:
        return "Moderate"
    elif score < 0.75:
        return "High"
    return "Extreme"
