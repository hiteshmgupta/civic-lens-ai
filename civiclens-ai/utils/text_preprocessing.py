"""
Text preprocessing utilities.
"""
import re


def clean_text(text: str) -> str:
    """Basic text cleaning for NLP processing."""
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    return text


def truncate(text: str, max_length: int = 512) -> str:
    """Truncate text to approximately max_length tokens (rough char estimate)."""
    char_limit = max_length * 4  # approximate chars per token
    if len(text) > char_limit:
        return text[:char_limit]
    return text
