import os

# Model Configuration
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SUMMARIZER_MODEL = "facebook/bart-large-cnn"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

# Stance labels for zero-shot classification
STANCE_LABELS = ["support", "oppose", "suggestion", "neutral"]

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", None)
