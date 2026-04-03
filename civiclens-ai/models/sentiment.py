"""
Sentiment Analysis using HuggingFace Inference API (async).
Model: cardiffnlp/twitter-roberta-base-sentiment-latest
Outputs scores in [-1, 1] range: negative=-1, neutral=0, positive=1.
"""
import logging
import re
from config import SENTIMENT_MODEL
import hf_client

logger = logging.getLogger(__name__)

POSITIVE_HINTS = {
    "support", "necessary", "critical", "essential", "welcome", "excellent",
    "important", "benefit", "improve", "effective", "protect", "security",
    "bargain", "invest", "coordination", "funding",
}

NEGATIVE_HINTS = {
    "concern", "concerned", "oppose", "failed", "failure", "insufficient",
    "cost", "costs", "bureaucratic", "inefficiencies", "inefficient",
    "surveillance", "blurred", "outdated", "expensive", "risk", "crowd",
    "neglects", "massive", "poor", "plagued",
}


def load_model():
    """No-op for API mode — kept for interface compatibility."""
    logger.info("Using HF Inference API for sentiment: %s", SENTIMENT_MODEL)


async def analyze(texts: list[str]) -> list[float]:
    """
    Analyze sentiment for a list of texts.
    Returns list of scores in [-1, 1].
    """
    if not texts:
        return []

    scores = []
    batch_size = 32
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            results = await hf_client.query(
                SENTIMENT_MODEL,
                {"inputs": batch}
            )
            for result in results:
                score = _convert_to_score(result)
                scores.append(score)
        except Exception as e:
            logger.error("Sentiment API call failed: %s", str(e))
            scores.extend(_heuristic_score(text) for text in batch)

    return scores


def get_distribution(scores: list[float]) -> dict:
    """Count positive, negative, neutral from scores."""
    dist = {"positive": 0, "negative": 0, "neutral": 0}
    for s in scores:
        if s > 0.1:
            dist["positive"] += 1
        elif s < -0.1:
            dist["negative"] += 1
        else:
            dist["neutral"] += 1
    return dist


def _convert_to_score(result: list[dict]) -> float:
    """Convert API output to single [-1, 1] score."""
    label_scores = {}
    for item in result:
        label = str(item.get("label", "")).lower().strip()
        score = float(item.get("score", 0.0))
        label_scores[label] = score

    # Handle both explicit labels and numeric labels used by some HF models.
    pos = label_scores.get("positive", label_scores.get("label_2", 0.0))
    neg = label_scores.get("negative", label_scores.get("label_0", 0.0))
    return pos - neg


def _heuristic_score(text: str) -> float:
    """Fallback sentiment score when the external model is unavailable."""
    tokens = re.findall(r"[a-z']+", text.lower())
    if not tokens:
        return 0.0

    pos_hits = sum(1 for token in tokens if token in POSITIVE_HINTS)
    neg_hits = sum(1 for token in tokens if token in NEGATIVE_HINTS)
    if pos_hits == 0 and neg_hits == 0:
        return 0.0

    score = (pos_hits - neg_hits) / max(pos_hits + neg_hits, 1)
    return max(-1.0, min(1.0, round(score, 4)))
