"""
Summarization using HuggingFace Inference API (async).
Model: facebook/bart-large-cnn for policy brief generation.
"""
import logging
from config import SUMMARIZER_MODEL
import hf_client

logger = logging.getLogger(__name__)


def load_model():
    """No-op for API mode — kept for interface compatibility."""
    logger.info("Using HF Inference API for summarization: %s", SUMMARIZER_MODEL)


async def summarize(amendment_text: str, comments: list[str]) -> str:
    """
    Generate a policy brief summary from the amendment text and public comments.
    """
    # Build context document
    context = f"Legislative Amendment:\n{amendment_text}\n\n"
    context += "Public Comments Summary:\n"

    sample = comments[:50] if len(comments) > 50 else comments
    for i, comment in enumerate(sample, 1):
        context += f"{i}. {comment}\n"

    # Truncate to model max (~1024 tokens ≈ 3000 chars for BART)
    if len(context) > 3000:
        context = context[:3000]

    try:
        result = await hf_client.query(
            SUMMARIZER_MODEL,
            {
                "inputs": context,
                "parameters": {
                    "max_length": 300,
                    "min_length": 15,
                    "do_sample": False,
                    "num_beams": 3,
                },
            },
        )

        if isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", "Summary generation failed.")
        return "Summary generation failed."

    except Exception as e:
        logger.error("Summarization API call failed: %s", str(e))
        return "Policy brief generation failed. Insufficient data for analysis."
