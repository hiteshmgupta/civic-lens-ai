"""
Sentiment Analysis using HuggingFace Inference API (async).
Model: cardiffnlp/twitter-roberta-base-sentiment-latest
Outputs scores in [-1, 1] range: negative=-1, neutral=0, positive=1.
"""
import logging
from config import SENTIMENT_MODEL
import hf_client

logger = logging.getLogger(__name__)


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
            scores.extend([0.0] * len(batch))

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
    label_scores = {item["label"].lower(): item["score"] for item in result}
    pos = label_scores.get("positive", 0)
    neg = label_scores.get("negative", 0)
    return pos - neg
