"""
Summarization using HuggingFace Inference API (async).
Model: facebook/bart-large-cnn for policy brief generation.
"""
import logging
import re
from collections import Counter
from config import SUMMARIZER_MODEL
import hf_client

logger = logging.getLogger(__name__)

STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "have", "will",
    "they", "their", "into", "about", "should", "would", "could", "them",
    "more", "than", "when", "what", "which", "while", "where", "been",
    "being", "were", "because", "there", "these", "those", "many", "much",
    "must", "need", "needs", "also", "very", "only", "does", "doing",
}


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
            summary = result[0].get("summary_text")
            if isinstance(summary, str) and summary.strip():
                return summary.strip()
        return _heuristic_summary(amendment_text, comments)

    except Exception as e:
        logger.error("Summarization API call failed: %s", str(e))
        return _heuristic_summary(amendment_text, comments)


def _heuristic_summary(amendment_text: str, comments: list[str]) -> str:
    """Local fallback summary when remote summarization is unavailable."""
    intro = amendment_text.strip().split(". ")
    amendment_summary = ". ".join(intro[:2]).strip()
    if amendment_summary and not amendment_summary.endswith("."):
        amendment_summary += "."

    comment_blob = " ".join(comments)
    tokens = [
        token for token in re.findall(r"[a-z']+", comment_blob.lower())
        if len(token) > 3 and token not in STOPWORDS
    ]
    common_terms = [word for word, _ in Counter(tokens).most_common(5)]

    support_signals = sum(1 for c in comments if any(word in c.lower() for word in ("support", "necessary", "welcome", "important", "critical")))
    concern_signals = sum(1 for c in comments if any(word in c.lower() for word in ("concern", "cost", "oppose", "bureaucratic", "surveillance", "failed")))

    stance_sentence = "Public feedback is mixed."
    if support_signals > concern_signals:
        stance_sentence = "Public feedback leans supportive, though some implementation concerns remain."
    elif concern_signals > support_signals:
        stance_sentence = "Public feedback leans cautious, with recurring concerns about cost, implementation, or scope."

    topics_sentence = ""
    if common_terms:
        topics_sentence = " Recurrent discussion topics include " + ", ".join(common_terms[:-1] + [common_terms[-1]]) + "."

    return f"{amendment_summary} {stance_sentence}{topics_sentence}".strip()
