import os

# HuggingFace Inference API
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
HF_API_URL = "https://api-inference.huggingface.co/models"

# Model names (same models, but now called via API instead of local)
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SUMMARIZER_MODEL = "facebook/bart-large-cnn"
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

# Stance labels for zero-shot classification
STANCE_LABELS = ["support", "oppose", "suggestion", "neutral"]

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
