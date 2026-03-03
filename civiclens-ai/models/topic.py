"""
Topic Modeling using BERTopic with sentence-transformer embeddings.
"""
import logging
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from config import EMBEDDING_MODEL, MODEL_CACHE_DIR

logger = logging.getLogger(__name__)

_embedding_model = None
_topic_model = None


def load_model():
    global _embedding_model, _topic_model
    logger.info("Loading embedding model: %s", EMBEDDING_MODEL)
    _embedding_model = SentenceTransformer(
        EMBEDDING_MODEL,
        cache_folder=MODEL_CACHE_DIR
    )
    logger.info("Embedding model loaded successfully")


def extract_topics(texts: list[str]) -> list[dict]:
    """
    Extract topic clusters from a list of texts.
    Returns list of {topic: str, size: int, keywords: list[str]}.
    """
    if not texts or len(texts) < 5:
        return [{"topic": "General Discussion", "size": len(texts), "keywords": []}]

    global _embedding_model, _topic_model

    if _embedding_model is None:
        load_model()

    try:
        embeddings = _embedding_model.encode(texts, show_progress_bar=False)

        # Configure BERTopic for small datasets
        min_topic_size = max(2, len(texts) // 10)
        _topic_model = BERTopic(
            embedding_model=_embedding_model,
            min_topic_size=min_topic_size,
            nr_topics="auto",
            verbose=False
        )

        topics, _ = _topic_model.fit_transform(texts, embeddings)

        # Extract topic info
        topic_info = _topic_model.get_topic_info()
        clusters = []
        for _, row in topic_info.iterrows():
            if row["Topic"] == -1:
                continue  # skip outlier topic
            topic_words = _topic_model.get_topic(row["Topic"])
            keywords = [word for word, _ in topic_words[:5]] if topic_words else []
            clusters.append({
                "topic": " | ".join(keywords[:3]) if keywords else f"Cluster {row['Topic']}",
                "size": int(row["Count"]),
                "keywords": keywords
            })

        # Sort by size descending
        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters[:10]  # top 10 clusters

    except Exception as e:
        logger.error("Topic modeling failed: %s", str(e))
        return [{"topic": "General Discussion", "size": len(texts), "keywords": []}]
