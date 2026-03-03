"""
Summarization using facebook/bart-large-cnn for policy brief generation.
"""
import logging
from transformers import pipeline
from config import SUMMARIZER_MODEL, MODEL_CACHE_DIR

logger = logging.getLogger(__name__)

_summarizer = None


def load_model():
    global _summarizer
    logger.info("Loading summarization model: %s", SUMMARIZER_MODEL)
    _summarizer = pipeline(
        "summarization",
        model=SUMMARIZER_MODEL,
        model_kwargs={"cache_dir": MODEL_CACHE_DIR} if MODEL_CACHE_DIR else {},
        truncation=True
    )
    logger.info("Summarization model loaded successfully")


def summarize(amendment_text: str, comments: list[str]) -> str:
    """
    Generate a policy brief summary from the amendment text and public comments.
    """
    if _summarizer is None:
        load_model()

    # Build context document
    context = f"Legislative Amendment:\n{amendment_text}\n\n"
    context += "Public Comments Summary:\n"

    # Take a representative sample if too many comments
    sample = comments[:50] if len(comments) > 50 else comments
    for i, comment in enumerate(sample, 1):
        context += f"{i}. {comment}\n"

    # Truncate to model max length (1024 tokens ≈ 3000 chars for BART)
    if len(context) > 3000:
        context = context[:3000]

    try:
        result = _summarizer(
            context,
            max_length=300,
            min_length=80,
            do_sample=False,
            num_beams=4
        )
        summary = result[0]["summary_text"]
        return summary
    except Exception as e:
        logger.error("Summarization failed: %s", str(e))
        return "Policy brief generation failed. Insufficient data for analysis."
