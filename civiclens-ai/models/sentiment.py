"""
Sentiment Analysis using cardiffnlp/twitter-roberta-base-sentiment-latest.
Outputs scores in [-1, 1] range: negative=-1, neutral=0, positive=1.
"""
import logging
from transformers import pipeline
from config import SENTIMENT_MODEL, MODEL_CACHE_DIR

logger = logging.getLogger(__name__)

_sentiment_pipeline = None


def load_model():
    global _sentiment_pipeline
    logger.info("Loading sentiment model: %s", SENTIMENT_MODEL)
    _sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL,
        tokenizer=SENTIMENT_MODEL,
        model_kwargs={"cache_dir": MODEL_CACHE_DIR} if MODEL_CACHE_DIR else {},
        top_k=None,
        truncation=True,
        max_length=512
    )
    logger.info("Sentiment model loaded successfully")


def analyze(texts: list[str]) -> list[float]:
    """
    Analyze sentiment for a list of texts.
    Returns list of scores in [-1, 1].
    """
    if not texts:
        return []

    if _sentiment_pipeline is None:
        load_model()

    scores = []
    # Process in batches of 32
    batch_size = 32
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        results = _sentiment_pipeline(batch)
        for result in results:
            score = _convert_to_score(result)
            scores.append(score)

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
    """Convert pipeline output to single [-1, 1] score."""
    label_scores = {item["label"].lower(): item["score"] for item in result}
    # Map: positive=+1, neutral=0, negative=-1
    pos = label_scores.get("positive", 0)
    neg = label_scores.get("negative", 0)
    neu = label_scores.get("neutral", 0)
    return pos - neg  # weighted sentiment in [-1, 1]
