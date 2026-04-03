"""
Zero-shot argument classification using HuggingFace Inference API (async).
Model: facebook/bart-large-mnli
Categories: support / oppose / suggestion / neutral.
"""
import logging
import re
from config import ZERO_SHOT_MODEL, STANCE_LABELS
import hf_client

logger = logging.getLogger(__name__)

SUPPORT_HINTS = {
    "support", "necessary", "essential", "welcome", "important", "critical",
    "benefit", "effective", "excellent", "absolutely", "bargain",
}
OPPOSE_HINTS = {
    "oppose", "concern", "concerned", "failed", "insufficient", "cost",
    "bureaucratic", "surveillance", "outdated", "poor", "inefficient",
    "blurred", "massive", "plagued",
}
SUGGESTION_HINTS = {
    "should", "could", "need", "needs", "include", "address", "consider",
    "recommend", "must", "requires",
}


def load_model():
    """No-op for API mode — kept for interface compatibility."""
    logger.info("Using HF Inference API for classification: %s", ZERO_SHOT_MODEL)


async def classify(texts: list[str]) -> dict:
    """
    Classify each text into stance categories.
    Returns:
      stance_counts: {support: int, oppose: int, suggestion: int, neutral: int}
      classified: list of (text, label) pairs
    """
    if not texts:
        return {"stance_counts": {l: 0 for l in STANCE_LABELS}, "classified": []}

    stance_counts = {label: 0 for label in STANCE_LABELS}
    classified = []

    for text in texts:
        try:
            result = await hf_client.query(
                ZERO_SHOT_MODEL,
                {
                    "inputs": text,
                    "parameters": {"candidate_labels": STANCE_LABELS},
                },
            )

            top_label = result["labels"][0]
            stance_counts[top_label] += 1
            classified.append((text, top_label))
        except Exception as e:
            logger.warning("Classification failed for text: %s", str(e))
            fallback_label = _heuristic_label(text)
            stance_counts[fallback_label] += 1
            classified.append((text, fallback_label))

    return {"stance_counts": stance_counts, "classified": classified}


def get_top_arguments(classified: list[tuple], label: str, top_n: int = 3) -> list[str]:
    """Get top N arguments for a given stance label."""
    matching = [text for text, lbl in classified if lbl == label]
    return matching[:top_n]


def _heuristic_label(text: str) -> str:
    """Fallback stance classification when zero-shot inference is unavailable."""
    tokens = set(re.findall(r"[a-z']+", text.lower()))
    support_hits = len(tokens & SUPPORT_HINTS)
    oppose_hits = len(tokens & OPPOSE_HINTS)
    suggestion_hits = len(tokens & SUGGESTION_HINTS)

    if suggestion_hits > max(support_hits, oppose_hits):
        return "suggestion"
    if support_hits > oppose_hits:
        return "support"
    if oppose_hits > support_hits:
        return "oppose"
    return "neutral"
