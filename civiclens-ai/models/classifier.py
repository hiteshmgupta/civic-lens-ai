"""
Zero-shot argument classification: support / oppose / suggestion / neutral.
"""
import logging
from transformers import pipeline
from config import ZERO_SHOT_MODEL, STANCE_LABELS, MODEL_CACHE_DIR

logger = logging.getLogger(__name__)

_classifier = None


def load_model():
    global _classifier
    logger.info("Loading zero-shot classifier: %s", ZERO_SHOT_MODEL)
    _classifier = pipeline(
        "zero-shot-classification",
        model=ZERO_SHOT_MODEL,
        model_kwargs={"cache_dir": MODEL_CACHE_DIR} if MODEL_CACHE_DIR else {},
    )
    logger.info("Zero-shot classifier loaded successfully")


def classify(texts: list[str]) -> dict:
    """
    Classify each text into stance categories.
    Returns:
      stance_counts: {support: int, oppose: int, suggestion: int, neutral: int}
      classified: list of (text, label) pairs
    """
    if not texts:
        return {"stance_counts": {l: 0 for l in STANCE_LABELS}, "classified": []}

    if _classifier is None:
        load_model()

    stance_counts = {label: 0 for label in STANCE_LABELS}
    classified = []

    batch_size = 16
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for text in batch:
            try:
                result = _classifier(
                    text,
                    candidate_labels=STANCE_LABELS,
                    truncation=True
                )
                top_label = result["labels"][0]
                stance_counts[top_label] += 1
                classified.append((text, top_label))
            except Exception as e:
                logger.warning("Classification failed for text: %s", str(e))
                stance_counts["neutral"] += 1
                classified.append((text, "neutral"))

    return {"stance_counts": stance_counts, "classified": classified}


def get_top_arguments(classified: list[tuple], label: str, top_n: int = 3) -> list[str]:
    """Get top N arguments for a given stance label."""
    matching = [text for text, lbl in classified if lbl == label]
    return matching[:top_n]
